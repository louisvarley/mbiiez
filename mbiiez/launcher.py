import os
import shutil
import subprocess
import time
import signal
import datetime
import shlex

from mbiiez.bcolors import bcolors
from mbiiez.conf import conf
from mbiiez import settings
from mbiiez.log_handler import log_handler
from mbiiez.process_handler import process_handler

class launcher: 

    # Names of various processes saved into database
    name_rtvrtm = "RTVRTM Service"
    name_dedicated = "Dedicated Server"
    name_auto_message = "Auto Message"
    name_log_watcher = "Log Watcher"

    event_handler = None
    log_handler = None
    config = None 
    instance_name = None 
    process_handler = None
    instance = None

    def __init__(self, instance):
        self.config = instance.config      
        self.log_handler = instance.log_handler
        self.process_handler = instance.process_handler
        self.instance_name = self.config['server']['name']
        self.instance = instance

    # Dedicated Server Thread
    def launch_dedicated_server_thread(self):   
        cmd = "nohup {} --quiet +set dedicated 2 +set net_port {} +set fs_game {} +exec {}".format(self.config['server']['engine'], self.config['server']['port'], settings.dedicated.game, self.config['server']['server_config_file']);
            
        self.log_handler.log("Command: " + cmd + "&")
        try:
            subprocess.check_call(shlex.split(cmd) ,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except Exception as e:
            self.log_handler.log("Dedicated Server process Crashed: {}".format(str(e)))       

        return
        
    # RTV/RTM Thread
    def launch_rtv_thread(self):
 
        self.log_handler.log("Launching RTV/RTM Instance...")
        cmd = "python /opt/openjk/rtvrtm.py -c {}".format(self.config['server']['rtvrtm_config_path']) 

        subprocess.check_call(shlex.split(cmd),stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        return
       
    # Auto Messaging Thread       
    def launch_auto_message_thread(self):             

        self.log_handler.log("Launching Auto Message Instance...")
        x = 0        
        while(True):
            for message in self.config['messages']['auto_messages']:
                time.sleep(60*int(self.config['messages']['auto_message_repeat_minutes']))                     
                try:
                    self.instance.say(message)
                except Exception as e:
                    self.log_handler.log("Was unable to send auto message to server: {}".format(str(e)))

        return
       
    # Dedicated Server Thread
    def launch_log_watch_thread(self):   
      
        try:
            self.log_handler.log_watcher()
        except Exception as e:
            self.instance.exception_handler.log(e)   
          
        return
                
    # Dedicated Server Launcher    
    def launch_dedicated_server(self):
    
        # Reason to Bail
        if(not os.path.isfile(self.config['server']['server_config_path'])):
            self.log_handler.log(bcolors.RED + "Failed to start. No config file found at {}".format(self.config['server']['server_config_path']) + bcolors.ENDC)        
            exit()
            
        # Reason to Bail  
        if(not os.path.isfile("{}/{}".format("/usr/bin", self.config['server']['engine']))):        
            self.log_handler.log(bcolors.RED + "Failed to start. No engine found at {}/{}".format("/usr/bin", self.config['server']['engine']) + bcolors.ENDC)   
            exit()
            
        # Make sure can be executed    
        os.system("chmod +x {}/{}".format("/usr/bin", self.config['server']['engine']))  
          
        # Sym Links
        if(os.path.exists("/root/.local/share/openjk")):
            if(not os.path.islink("/root/.local/share/openjk")):
                shutil.rmtree("/root/.local/share/openjk")       
                os.symlink(settings.locations.game_path, "/root/.local/share/openjk")
        
        if(os.path.exists("/root/.ja")):
            if(not os.path.islink("/root/.ja")):
                shutil.rmtree("/root/.ja")       
                os.symlink(settings.locations.game_path, "/root/.ja")  
    
        self.process_handler.add(self.launch_dedicated_server_thread, self.name_dedicated, self.instance_name)

    # RTV/RTM Launcher
    def launch_rtv(self): 

        # RTV RTM
        if(self.config['server']['enable_rtv'] == True or self.config['server']['enable_rtm']):  
            if(not os.path.isfile("{}/{}".format(settings.locations.mbii_path, self.config['server']['rtvrtm_config_file']))):
                self.log_handler.log(bcolors.RED + "Unable to find RTV/RTV config. RTV/RTM will not run")
                      
        self.process_handler.add(self.launch_rtv_thread, self.name_rtvrtm, self.instance_name)

    # Auto Messaging Launcher
    def launch_auto_message(self):
    
        if(self.config['messages']['auto_message_enable']):                    
            self.process_handler.add(self.launch_auto_message_thread, self.name_auto_message, self.instance_name)
            
    def launch_log_watch(self):             
        self.process_handler.add(self.launch_log_watch_thread, self.name_log_watcher, self.instance_name)
    