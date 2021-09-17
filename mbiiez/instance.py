import shutil
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

        self.start_cmd = None

        # Generate Config for this instance 
        self.conf = conf(self.name, settings)       
        self.config = self.conf.config

        if(self.config == None):
            print("No Instance config for {}".format(name))
            exit()
            
        self.plugins = self.config['plugins']
        self.plugins_registered = []

        self.log_handler = log_handler(self)
        self.exception_handler = exception_handler(self)
        self.process_handler = process_handler(self)
        self.launcher = launcher(self)
        self.event_handler = event_handler(self)        
        self.db = db()
        
        # Create a UDP / RCON Client
        self.console = console(self.config['security']['rcon_password'], str(self.config['server']['port']))
        
        # Load Internal Services
        self.services_internal()

        # Load Internal Events
        self.events_internal()

        #Load Plugins
        self.plugin_hander = plugin_handler(self)
        
        ''' Add any configs to external plugins if they are enabled '''    
        ''' if(self.has_plugin("auto_message")):
            self.config['plugins']['auto_message']['messages'].append("This server is powered by MBIIEZ, visit bit.ly/2JhJRpO") '''   

    def services_internal(self):
        ''' Internal Services we wish to start on an instance start ''' 

        ''' Runs the Dedicated OpenJK Server ''' 
        cmd = "{} --quiet +set dedicated 2 +set net_port {} +set fs_game {} +exec {}".format(self.config['server']['engine'], self.config['server']['port'], self.get_game(), self.config['server']['server_config_file']);       
        
        self.start_cmd = cmd
        
        print(cmd)
        self.process_handler.register_service("OpenJK", cmd, 1) 
        
        ''' Log Watcher Service ''' 
        self.process_handler.register_service("Log Watcher", self.log_handler.log_watcher)
        
        ''' Restarter Service '''
        self.process_handler.register_service("Scheduled Restarter", self.event_handler.restarter)

        ''' RTV Service, Eventually move to a plugin ''' 
        if(self.config['server']['enable_rtv']):
            cmd = "python /opt/openjk/rtvrtm.py -c {}".format(self.config['server']['rtvrtm_config_path']) 
            self.process_handler.register_service("RTVRTM", cmd, 999, self.log_handler.log_await) 
            
    def events_internal(self):
        ''' Events we wish to run internal methods on '''
        self.event_handler.register_event("player_chat_command", self.event_handler.player_chat_command)
        self.event_handler.register_event("player_chat", self.event_handler.player_chat)
        self.event_handler.register_event("player_chat_team", self.event_handler.player_chat_team)
        self.event_handler.register_event("player_killed", self.event_handler.player_killed)       
        self.event_handler.register_event("player_connected", self.event_handler.player_connected)               
        self.event_handler.register_event("player_disconnected", self.event_handler.player_disconnected)       
        self.event_handler.register_event("player_begin", self.event_handler.player_begin)          
        self.event_handler.register_event("player_info_change", self.event_handler.player_info_change)          
        return
        
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
           
    # True / False is server empty       
    def is_empty(self):
        if(self.players_count() > 0):
            return False
        else:
            return True
           
    # Int of the number of players in game        
    def players_count(self):
        return len(self.players())
            
    # Get list of players in game - Avoid client for quickness
    def players(self):
        
        players = []        
        status = self.console.console("getstatus", True)
        
        if(status == None):
            return {}
        
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
    
        self.stop()
        time.sleep(1)
        
        print("Running Command: {}" + self.start_cmd)

        # Generate our configs
        self.conf.generate_server_config()
        self.conf.generate_rtvrtm_config()
        self.conf.generate_rtvrtm_map_lists()
        
        if(self.server_running()):
             print(bcolors.OK + "Instance is already running" + bcolors.ENDC)
             return;
        
        # Can Instance Can Start?
        if(os.path.exists(self.config['server']['server_config_path'])): 

            # Reason to Bail  
            if(not os.path.isfile("{}/{}".format("/usr/bin", self.config['server']['engine']))):        
                self.log_handler.log(bcolors.RED + "Failed to start. No engine found at {}/{}".format("/usr/bin", self.config['server']['engine']) + bcolors.ENDC)   
                print(bcolors.FAIL + "[Error] " + bcolors.ENDC + "Failed to start. No engine found at {}/{}".format("/usr/bin", self.config['server']['engine']))
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
        
                           
            self.event_handler.run_event("before_launch_server")
            self.process_handler.launch_services()
     
      
        else:
            print(bcolors.FAIL + "[Error] " + bcolors.ENDC + "Unable to Load a SERVER config at " + self.config['server']['server_config_path'])
            print(bcolors.FAIL + "Unable to proceed without a valid Server Config File" + bcolors.ENDC)
            
    def server_running(self):
    
        if(self.process_handler.process_status_name("OpenJK")):
            return True
        else:
            return False
                
    def rtv_running(self):
        result = subprocess.run(['ps', 'ax'], stdout=subprocess.PIPE)
        output = str(result.stdout.decode())
        for item in output.splitlines():
            if(self.config['server']['rtvrtm_config_file'] in item):
                return True
        
    def has_plugin(self, plugin_name):
    
        if(plugin_name in self.config['plugins']):
            return True
        else:
            return False
            
    def get_game(self):
    
         # Allows GAME override using JSON
        game = settings.dedicated.game
        
        if("game" in self.config['server'].keys()):           
            game = self.config['server']['game']
            
        return game    
                
    # Instance Status Information
    def status(self):

        print("------------------------------------") 
        
        if(self.server_running()):
        
            players = self.players()
 
            print(bcolors.CYAN + "Instance Name: " + bcolors.ENDC + self.name)   
            print(bcolors.CYAN + "Server Name: " + bcolors.ENDC + bcolors().color_convert(self.config['server']['host_name']))
            print(bcolors.CYAN + "Game: " + bcolors.ENDC + self.get_game())              
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
     
        for service in self.process_handler.services:
                if(self.process_handler.process_status_name(service['name'])):
                    print("[{}Yes{}] {} Running".format(bcolors.GREEN, bcolors.ENDC, service['name']))
                else:
                    print("[{}No{}] {} Running".format(bcolors.RED, bcolors.ENDC, service['name']))
            

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

        if(os.path.exists(self.config['server']['log_path'])):
            os.remove(self.config['server']['log_path'])        
    
    # Stop then start the instance
    def restart(self):     
        self.stop()
        time.sleep(2)
        self.start()           
                        

