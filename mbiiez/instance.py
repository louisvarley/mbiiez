import sys, getopt
import os
import subprocess
import re
import urllib.request
import shlex
import psutil
import time
import prettytable

from mbiiez.bcolors import bcolors
from mbiiez.helpers import helpers
from mbiiez.testing import testing
from mbiiez.conf import conf
from mbiiez.console import console
from mbiiez.db import db
from mbiiez.launcher import launcher
from mbiiez.log_handler import log_handler
from mbiiez.exception_handler import exception_handler
from mbiiez.process_handler import process_handler
from mbiiez.event_handler import event_handler
from mbiiez.plugin_handler import plugin_handler
from mbiiez.models import chatter, log

from mbiiez import settings

# An Instance of MBII                        
class instance:

    name = None
    config = None
    external_ip = None
    console = None
    conf = None
    db = None
    
    log_handler = None
    exception_handler = None
    event_handler = None
    process_handler = None
    plugin_handler = None
    launcher = None
    
    # Constructor
    def __init__(self, name):
    
        self.name = name
        self.external_ip = urllib.request.urlopen('http://ip.42.pl/raw').read().decode()       
        self.conf = conf(self.name, settings.locations.script_path, settings.locations.mbii_path)
        self.config = self.conf.config
        self.plugins = self.config['plugins']
        self.plugins_registered = []

        self.log_handler = log_handler(self)
        self.exception_handler = exception_handler(self)
        self.process_handler = process_handler(self)
        self.launcher = launcher(self)
        self.event_handler = event_handler(self)        
        self.db = db()
        
        self.plugin_hander = plugin_handler(self)

        # Create a UDP / RCON Client
        self.console = console(self.config['security']['rcon_password'], str(self.config['server']['port']))
        
    # Use netstat to get the port used by this instance
    def get_port(self):  
        port = 0
        response =  os.system("netstat -tulpn | grep {}".format(settings.dedicated.engine))
        for item in response.splitlines():
            if settings.dedicated.engine in item:
                port = item.split()[3].split(":")[1];   

        if(int(port) > 0):
            return str(port)  

        return None  

    # Is RTV / RTM Service running and instance
    def get_rtv_status(self):  
    
        response =  os.system("ps ax | grep {}".format("rtvrtm.py"))
        for item in response.splitlines():
            if("rtvrtm" in item):
                return(True) 
                
        return False  

    # Is the chosen engine running an instance
    def get_ded_engine_status(self):  

        response =  os.system('ps ax | grep {}'.format(settings.dedicated.engine))
        for item in response.splitlines():
            if(settings.dedicated.engine in item):
                return(True) 
                
        return False  

    # Run an RCON command
    def rcon(self, command):
        print(self.console.rcon(str(command), False))
       
    # Run a console command
    def cmd(self, command):
        print(self.console.console(str(command), False))      
       
    # Get / Set a CVAR
    def cvar(self, key, value = None):
       return self.console.cvar(key, value)   
       
    # Run an SVSAY command
    def say(self, message):
        self.console.say(message)
       
    # Run an SVTELL command
    def tell(self, player_id, message):
        self.console.tell(player_id, message)       
       
    # Get / Set current map
    def map(self, map_name = None):
    
         if(not map_name == None):
            self.console.rcon("map " + map_name, True)
            print("Map change requested to {}".format(map_name))
            return True
         else:
            try:
                server_map = self.cvar("mapname")
               
            except:
                server_map = "Error while fetching"
            
            return server_map        
        
    # Get / Set current mode
    def mode(self, mode = None):   

        if(not mode == None):
            self.cvar("g_authenticity", mode)
            print("Mode change requested to Mode {}".format(mode))
            return True
        else:   
            mode = self.cvar("g_authenticity")

        try:
            
            #0 = Open mode, 1 = Semi-Authentic, 2 = Full-Authentic, 3 = Duel, 4 = Legends
            if(mode == "0"):
                return "Open"
            if(mode == "1"):
                return "Semi-Authentic"
            if(mode == "2"):
                return "Full-Authentic"
            if(mode == "3"):
                return "Duel"
            if(mode == "4"):                
                return "Legends"     
                    
        except:
           mode = "Error while fetching"
        
        return mode  

    # Server uptime as a string
    def uptime(self):

        uptime = "unknown"      
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
        output = str(result.stdout.decode())
        
        for item in output.splitlines():
            if(self.config['server']['server_config_file'] in item):
                uptime = (item.split()[9])      

        return uptime 
 
    # Kick a player
    def kick(self, player):
        self.console.rcon("kick " + player)
        
    # Ban a player    
    def ban(self, ip):
        self.console.rcon("addip " + ip)
       
    # Unban a player
    def unban(self, ip):
        self.console.rcon("removeip " + ip)
       
    # List banned players
    def listbans(self):
        self.console.rcon("g_banips")
           
    # Int of the number of players in game        
    def players_count(self):
        return len(self.players())
            
    # Get list of players in game
    def players(self):
        
        players = []        
        status = self.console.console("getstatus", True)
        status = status.split("\n")

        x = 2
        while(x < int(len(status)-1)):
            line = str(status[x])
            line_split = shlex.split(line)
            player = bcolors().color_convert(line_split[2])
            ping = line_split[1]
            
            if(int(ping) < 100):
                ping = bcolors.GREEN + ping + bcolors.ENDC           
            elif(int(ping) < 150):
                ping = bcolors.YELLOW + ping + bcolors.ENDC           
            else:
                ping = bcolors.RED + ping + bcolors.ENDC
            
            ping = bcolors().color_convert(ping)
            
            players.append({"name":player, "ping": ping})
            x = x + 1
   
        return players
        
    # Print the server log
    def log(self):
        print("do to")
        
    # Run an automated test on a number of things printing results
    def test(self):

        lookup = helpers().ip_info()
        print("Server IP {}".format(self.external_ip))
        print("Server Location {}".format(lookup['region']))
        print("-------------------------------------------")
        print("CA Central: " + testing().ping_test("35.182.0.251"))   
        print("EU East: " + testing().ping_test("35.178.0.253"))
        print("EU Central: " + testing().ping_test("18.196.0.253"))
        print("EU West: " + testing().ping_test("34.240.0.253"))
        print("US WEST: " + testing().ping_test("52.52.63.252"))
        print("US EAST: " + testing().ping_test("35.153.128.254"))
        print("-------------------------------------------")
        print("CPU Usage: {}%".format(str(psutil.cpu_percent())))
        print("Memory Usage: {}%".format(str(psutil.virtual_memory().percent)))       
         
    # Start this instance
    def start(self):

        # Generate our configs
        self.conf.generate_server_config()
        self.conf.generate_rtvrtm_config()
        self.conf.generate_rtvrtm_map_lists()
        
        if(self.server_running()):
             print(bcolors.OK + "Instance is already running" + bcolors.ENDC)
             return;
        
        # Can Instance Can Start?
        if(os.path.exists(self.config['server']['server_config_path'])):
            print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Launching Dedicated Server")
            
            self.event_handler.run_event("before_launch_server")
            self.launcher.launch_dedicated_server()
            
            print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Launching Log Watch Service")
            self.launcher.launch_log_watch()
            
            if(self.config['messages']['auto_message_enable'] and len(self.config['messages']['auto_messages']) > 0):
                print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Launching Auto Message Service") 
                self.launcher.launch_auto_message()
            
            if(os.path.exists(self.config['server']['rtvrtm_config_path'])):
                
                if(self.config['server']['enable_rtv']):
                    print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Launching RTV/RTM Service")               
                    self.launcher.launch_rtv()
      
        else:
            print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Unable to Load a SERVER config at " + self.config['server']['server_config_path'])
            print(bcolors.FAIL + "Unable to proceed without a valid Server Config File" + bcolors.ENDC)
            


    def server_running(self):
    
        if(self.process_handler.process_status(self.launcher.name_dedicated)):
            return True
        else:
            return False
                
    def rtv_running(self):
        result = subprocess.run(['ps', 'ax'], stdout=subprocess.PIPE)
        output = str(result.stdout.decode())
        for item in output.splitlines():
            if(self.config['server']['rtvrtm_config_file'] in item):
                return True
                
    # Instance Status Information
    def status(self):

        print("------------------------------------") 
        
        if(self.server_running()):
        
            players = self.players()
 
            print(bcolors.CYAN + "Instance Name: " + bcolors.ENDC + self.name)   
            print(bcolors.CYAN + "Server Name: " + bcolors.ENDC + bcolors().color_convert(self.config['server']['host_name']))    
            print(bcolors.CYAN + "Engine: " + bcolors.ENDC + self.config['server']['engine'])           
            print(bcolors.CYAN + "Port: " + bcolors.ENDC + str(self.config['server']['port']))                
            print(bcolors.CYAN + "Full Address: " + bcolors.ENDC + self.external_ip + ":" + str(self.config['server']['port']))
            print(bcolors.CYAN + "Mode: " + bcolors.ENDC + self.mode(None))   
            print(bcolors.CYAN + "Map: " + bcolors.ENDC + self.map(None)) 
            print(bcolors.CYAN + "Plugins: " + bcolors.ENDC + ",".join(self.plugins_registered))
            
            print(bcolors.CYAN + "Uptime: " + bcolors.ENDC + self.uptime())
            if(len(players) > 0):
                print(bcolors.CYAN + "Players: " + bcolors.ENDC + bcolors.GREEN + str(len(players)) + "/32" + bcolors.ENDC) 
            else:
                print(bcolors.CYAN + "Players: " + bcolors.ENDC + bcolors.RED + str(len(players)) + "/32" + bcolors.ENDC)                   
            
                
            
        print("------------------------------------")    
        if(self.server_running()):
            print("[{}Yes{}] OpenJK Server Running".format(bcolors.GREEN, bcolors.ENDC))
        else:          
            print("[{}No{}] OpenJK Server Running".format(bcolors.RED, bcolors.ENDC))    
            
        if(self.process_handler.process_status(self.launcher.name_rtvrtm)):
            print("[{}Yes{}] RTV/RTM Service Running".format(bcolors.GREEN, bcolors.ENDC))  
        else:          
            print("[{}No{}] RTV/RTM Service Running".format(bcolors.RED, bcolors.ENDC))    

        if(self.process_handler.process_status(self.launcher.name_auto_message)):
            print("[{}Yes{}] Auto Server Messages".format(bcolors.GREEN, bcolors.ENDC))  
        else:          
            print("[{}No{}] Auto Server Messages".format(bcolors.RED, bcolors.ENDC))    

        if(self.process_handler.process_status(self.launcher.name_log_watcher)):
            print("[{}Yes{}] Log Monitoring Service Running".format(bcolors.GREEN, bcolors.ENDC))  
        else:          
            print("[{}No{}] Log Monitoring Service Running".format(bcolors.RED, bcolors.ENDC))    


        if(self.server_running()):        
            if(len(players) > 0):
                x = prettytable.PrettyTable()
                x.field_names = list(players[0].keys())
                for player in players:
                    x.add_row(player.values())
                print(x)
            else:
                print("-------------------------------------------")
                print(bcolors.RED + "No one is playing"  + bcolors.ENDC )   

            print("-------------------------------------------")            
                
    # Stop the instance
    def stop(self):
        self.process_handler.stop_all()
    
    # Stop then start the instance
    def restart(self):     
        self.stop()
        time.sleep(2)
        self.start()           
                        

