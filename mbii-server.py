#!/usr/bin/python3

import json
import os
import glob
import shutil
import psutil
import subprocess
import time
import threading
import watchgod
import signal
import six
import sys
import datetime

from app.mbii.bcolors import bcolors
from app.mbii.helpers import helpers
from app.mbii.testing import testing
from app.mbii.config_manager import config_manager
from app.mbii.process_manager import process_manager
from app.mbii.mbii_manager import mbii_manager
from app.mbii.udp_client import udp_client
from app.mbii.globals import globals
 
class launcher: 

    event_handler = None
    log_handler = None
    config = None 
   
    game_crashes = 0
    rtv_crashes = 0 
    max_tries = 5

    def __init__(self, config, event_handler, log_handler):
        self.config = config
        self.event_handler = event_handler
        self.log_handler = log_handler
        
    # PreLaunch RTV/RTM Setup    
    def setup_rtv(self):

        # RTV RTM
        if(self.config['server']['enable_rtv'] == True or self.config['server']['enable_rtm']):  
            if(not os.path.isfile("{}/{}".format(globals.mbii_path, self.config['server']['rtvrtm_config_file']))):
                self.log_handler.log(bcolors.RED + "Unable to find RTV/RTV config. RTV/RTM will not run")
                      
    # PreLaunch Dedicated Server Setup        
    def setup_game(self):
 
        # Reason to Bail
        if(not os.path.isfile(self.config['server']['server_config_path'])):
            self.log_handler.log(bcolors.RED + "Failed to start. No config file found at {}".format(self.config['server']['server_config_path']))        
            exit()
            
        # Reason to Bail  
            self.log_handler.log(bcolors.RED + "Failed to start. No engine found at {}/{}".format("/usr/bin", globals.engine))   
            exit()
            
        os.system("chmod +x {}/{}".format(globals.game_path, globals.engine))  
          
        # Sym Links
        if(os.path.exists("/root/.local/share/openjk")):
            if(not os.path.islink("/root/.local/share/openjk")):
                shutil.rmtree("/root/.local/share/openjk")       
                os.symlink(globals.game_path, "/root/.local/share/openjk")
        
        if(os.path.exists("/root/.ja")):
            if(not os.path.islink("/root/.ja")):
                shutil.rmtree("/root/.ja")       
                os.symlink(globals.game_path, "/root/.ja")        
        
    # Dedicated Server Thread
    def launch_game_thread(self):   
        if(self.event_handler.is_running() and self.game_crashes < 5):
            self.log_handler.log(bcolors.GREEN + "Launching dedicated server instance...")
            cmd = "{} +set dedicated 2 +set net_port {} +set fs_game {} +exec {}".format(globals.engine, self.config['server']['port'], globals.game, self.config['server']['server_config_file']);
            
            self.log_handler.log("Running: " + cmd)
            os.system(cmd)
            
            if(self.event_handler.is_running()):
                self.game_crashes += 1
                self.log_handler.log(bcolors.RED + "Dedicated server Crashed {} times, Restarting...".format(str(self.game_crashes)))   
            self.launch_game() 

        if(self.game_crashes >= self.max_tries):
            self.log_handler.log(bcolors.RED + "Dedicated Server Crashed {} times and will stop...".format(str(self.game_crashes)))            
            
        return
        
    # RTV/RTM Thread
    def launch_rtv_thread(self):
        if(self.event_handler.is_running()  and self.rtv_crashes < 5):
            self.log_handler.log(bcolors.GREEN + "Launching RTV/RTM instance...")
            self.log_handler.log("python /opt/openjk/rtvrtm.py -c {}".format(self.config['server']['rtvrtm_config_path']))
            os.system("python /opt/openjk/rtvrtm.py -c {}".format(self.config['server']['rtvrtm_config_path']))
            if(self.event_handler.is_running()):
                self.rtv_crashes += 1
                self.log_handler.log(bcolors.RED + "RTV/RTM Service Crashed {} times, Restarting...".format(str(self.rtv_crashes)))
            self.launch_rtv()
            
        if(self.rtv_crashes >= self.max_tries):
            self.log_handler.log(bcolors.RED + "RTV/RTM Service Crashed {} times and will stop...".format(str(self.rtv_crashes)))   
                        
            
        return
       
    # Auto Messaging Thread       
    def launch_auto_message_thread(self):             
        if(self.event_handler.is_running()):
            self.log_handler.log(bcolors.GREEN + "Launching Auto Message instance..." + bcolors.ENDC)
            client = udp_client(self.config['security']['rcon_password'], self.config['server']['port'])
            x = 0        
            while(True):
                for message in self.config['messages']['auto_messages']:
                    time.sleep(60*int(self.config['messages']['auto_message_repeat_minutes']))                     
                    try:
                        client.say(message)
                    except Exception as e:
                        self.log_handler.log("Was unable to send auto message to server: {}".format(str(e)))
            if(self.event_handler.is_running()):
                self.log_handler.log("Auto messager crashed and has been restarted...")   
            self.launch_auto_message()
        return
       
    # Dedicated Server Launcher    
    def launch_game(self):
        thread = threading.Thread(target=self.launch_game_thread)
        thread.daemon = True
        thread.start()
        self.event_handler.add_thread(thread)
        return thread

    # RTV/RTM Launcher
    def launch_rtv(self):  
        thread = threading.Thread(target=self.launch_rtv_thread)
        thread.daemon = True
        thread.start()
        self.event_handler.add_thread(thread)       
        return thread

    # Auto Messaging Launcher
    def launch_auto_message(self):
        if(self.config['messages']['auto_message_enable']):
            print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)  
            print(bcolors.GREEN + "Auto Message Enabled" + bcolors.ENDC)                         
            thread = threading.Thread(target=self.launch_auto_message_thread)
            thread.daemon = True
            thread.start()
            self.event_handler.add_thread(thread)
            return thread
    
class event_handler:

    running = False
    threads = []
    config = None
    log_handler = None
    process_manager = None
    
    def __init__(self, config, log_handler):
        self.config = config
        self.log_handler = log_handler
        self.process_manager = process_manager()
    
    def add_thread(self, thread):
        self.threads.append(thread)
        self.log_handler.log("New Thread")
    
    def start(self):
        self.running = True
        
    def stop(self):
        self.running = False
    
    def is_running(self):
        return self.running
        
    def shutdown(self, signal, frame):    
        self.log_handler.log(bcolors.RED + "Gracefull shutdown...")
        self.stop()  
        
        # Had trouble ending processes using threads so process_manager brute forces by their config files
        self.process_manager.kill_process_by_name(self.config['server']['server_config_file'])
        self.process_manager.kill_process_by_name(self.config['server']['rtvrtm_config_file'])
        os.system("reset")    
        exit()

class log_handler:

    client = None
    config = None

    def __init__(self, config):
        self.config = config
        self.client = udp_client(self.config['security']['rcon_password'], self.config['server']['port'])

    def get_last_line(self, file):
        line = subprocess.check_output(['tail', '-1', file])
        return line

    def log(self, log_line):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.config['server']['log_path'], "a") as logFile:
            log_line = dt + ":" + log_line + bcolors.ENDC
            print(log_line)
            log_line = helpers().ansi_strip(log_line)           
            logFile.write(log_line + "\n")

    def log_changed(self):

        last_line = self.get_last_line(self.config['server']['log_path']).decode();

        if('!hello' in last_line):
            self.client.say("Hello There")
             
        #If Change contains ClientConnect: (^3|NR|^5SEAL^7TeamRicks) ID: 0 (IP: 86.189.246.246:29070)
        #Send Player Connected
        
        #If ClientDisconnect: 0
        #Send Player Disconnected  

        #If 0: say: ^3|NR|^5SEAL^7TeamRicks: "!report something something"
        #Send Moderator Report
        
        #If Kill: 4 1 86: ^3|NR|^5SEAL^7TeamRicks killed ^7|^3NR^7|Zitnar|^3INI^7| by MOD_SABER
        #Send a Kill

class main:

    name = None
    log_handler = None
    event_handler = None
    launcher = None
    config_manager = None
    config = None

    def start(self, name):
    
        self.name = name

        self.config_manager = config_manager(self.name, globals.script_path, globals.mbii_path)
        self.config = self.config_manager.config
       
        self.log_handler = log_handler(self.config)
        self.event_handler = event_handler(self.config, self.log_handler)
        
        self.launcher = launcher(self.config, self.event_handler, self.log_handler)

        self.event_handler.start()

        print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)   
        print(bcolors.GREEN + "Starting Server Instance..." + bcolors.ENDC)
        print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)   

        self.log_handler.log("Starting server instance...")

        self.launcher .setup_rtv()
        self.launcher .setup_game()
        self.launcher .launch_auto_message()
        self.launcher .launch_rtv()
        self.launcher .launch_game()

        print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)   
        print(bcolors.GREEN + "Ctrl + C to exit..." + bcolors.ENDC)
        print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)    
        
        #This ensures on shutdown, all spanwed processes are cleared up
        #signal.signal(signal.SIGINT, self.event_handler.keyboardInterruptHandler)
        
        signal.signal(signal.SIGINT, self.event_handler.shutdown)
        signal.signal(signal.SIGTERM, self.event_handler.shutdown)

        while (True):       
            for changes in watchgod.watch(self.config['server']['log_path']):
                self.log_handler.log_changed()
                    

        
if __name__ == "__main__":

    name = sys.argv[1]
    if(name == None):
        print("Usage: mbii-server *INSTANCE*")
        
    main().start(name)
           
