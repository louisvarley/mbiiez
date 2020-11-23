#!/usr/bin/python3

import sys, getopt
import os
import subprocess
import re
import urllib.request
import argparse
import json
import six
import binascii
import shlex
import psutil
import time
import json


from app.mbii.bcolors import bcolors
from app.mbii.helpers import helpers
from app.mbii.testing import testing
from app.mbii.config_manager import config_manager
from app.mbii.process_manager import process_manager
from app.mbii.mbii_manager import mbii_manager
from app.mbii.udp_client import udp_client
from app.mbii.globals import globals
 
from subprocess import Popen, PIPE, STDOUT


                                   
# An Instance of MBII                        
class server_instance:

    name = None
    config_manager = None
    external_ip = None
    udp_client = None
    config = None
    
    # Constructor
    def __init__(self, name):
    
        self.name = name
        self.external_ip = urllib.request.urlopen('http://ip.42.pl/raw').read().decode()       
        self.config_manager = config_manager(self.name, globals.script_path, globals.mbii_path)

        self.config = self.config_manager.config

        self.process_manager = process_manager()

        # Create a UDP / RCON Client
        self.udp_client = udp_client(self.config['security']['rcon_password'], str(self.config['server']['port']))
        
       
    # Use netstat to get the port used by this instance
    def get_port(self):  
        port = 0
        response =  os.system("netstat -tulpn | grep {}".format(globals.engine))
        for item in response.splitlines():
            if globals.engine in item:
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

        response =  os.system('ps ax | grep {}'.format(globals.engine)) #FYI Using Bars to merely return a 0 or 1 with GREP causing an error so doing parsing line by line here
        for item in response.splitlines():
            if(globals.engine in item):
                return(True) 
                
        return False  

    # Run an RCON command
    def rcon(self, command):
        return self.udp_client.rcon(str(command))
       
    # Run a console command
    def console(self, command):
        return self.udp_client.console(command, True)       
       
    # Get / Set a CVAR
    def cvar(self, key, value = None):
       return self.udp_client.cvar(key, value)   
       
    # Run an SVSAY command
    def say(self, message):
        self.udp_client.say(message)
       
    # Get / Set current map
    def map(self, map_name = None):
    
         if(not map_name == None):
            self.udp_client.rcon("map " + map_name, True)
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
        self.udp_client.rcon("kick " + player)
        
    # Ban a player    
    def ban(self, ip):
        self.udp_client.rcon("addip " + ip)
       
    # Unban a player
    def unban(self, ip):
        self.udp_client.rcon("removeip " + ip)
       
    # List banned players
    def listbans(self):
        self.udp_client.rcon("g_banips")
           
    # Int of the number of players in game        
    def players_count(self):
        return len(self.players())
            
    # Get list of players in game
    def players(self):
        
        players = []
        
        status = self.console("getstatus")
        status = status.split("\n")
        
        x = 2
        while(x < int(len(status)-1)):
            line = str(status[x])
            line_split = shlex.split(line)
            player = line_split[2]
            ping = line_split[1]
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

        # Instance Running
        if(process_manager().pid_file_running(self.config['server']['pid_file'])):
            print(bcolors.OK + "Instance is already running..." + bcolors.ENDC)  
            return
            
        # Generate our configs
        self.config_manager.generate_server_config()
        self.config_manager.generate_rtvrtm_config()
        self.config_manager.generate_rtvrtm_map_lists()
                          
        # Instance Can Start
        if(os.path.exists(self.config['server']['server_config_path'])):
            print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Loaded SERVER config")
                         
            if(os.path.exists(self.config['server']['rtvrtm_config_path'])):
                print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Loaded RTVRTM config")
                
                if(self.config['server']['enable_rtv']):
                    print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Enable Rock the Vote")               
                else:
                    print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Enable Rock the Vote")              
                if(self.config['server']['enable_rtm']):
                    print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Enable Rock the Mode")               
                else:
                    print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Enable Rock the Mode")                 
                
            else:
            
                if(self.config['server']['enable_rtv'] or self.config['server']['enable_rtm']):
                    print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Unable to Load RTVRTM config at " +  self.config['server']['rtvrtm_config_path'] + bcolors.ENDC)                             
                    
                print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Enable Rock the Vote")   
                print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Enable Rock the Mode")   

            print("-------------------------------------------")

            pid = subprocess.Popen(["mbii-server", self.name], shell=False, cwd=globals.script_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).pid

            # Save Process PID
            f = open(self.config['server']['pid_file'], "w")
            f.write(str(pid))
            f.close()
                        
        else:
            print(bcolors.FAIL + "[No] " + bcolors.ENDC + "Unable to Load SERVER config at " + self.config['server']['server_config_path'])
            print(bcolors.FAIL + "Unable to proceed without a valid Server Config File" + bcolors.ENDC)
            exit()

    def server_running(self):
        result = subprocess.run(['ps', 'ax'], stdout=subprocess.PIPE)
        output = str(result.stdout.decode())
        for item in output.splitlines():
            if(self.config['server']['server_config_file'] in item):
                return True
                
    def rtv_running(self):
        result = subprocess.run(['ps', 'ax'], stdout=subprocess.PIPE)
        output = str(result.stdout.decode())
        for item in output.splitlines():
            if(self.config['server']['rtvrtm_config_file'] in item):
                return True
                
    # Instance Status Information
    def status(self):

        dedicated_running = False
        
                
        print("-------------------------------------------")
        
        if(self.server_running()):
        
            players = self.players()
        
            print(bcolors.CYAN + "Instance Name: " + bcolors.ENDC + self.name.upper())   
            print(bcolors.CYAN + "Server Name: " + bcolors.ENDC + bcolors().color_convert(self.config['server']['host_name']))            
            print(bcolors.CYAN + "Port: " + bcolors.ENDC + str(self.config['server']['port']))                
            print(bcolors.CYAN + "Full Address: " + bcolors.ENDC + self.external_ip + ":" + str(self.config['server']['port']))
            print(bcolors.CYAN + "Mode: " + bcolors.ENDC + self.mode(None))   
            print(bcolors.CYAN + "Map: " + bcolors.ENDC + self.map(None))              
            print(bcolors.CYAN + "Uptime: " + bcolors.ENDC + self.uptime())      
            print(bcolors.CYAN + "Players: " + bcolors.ENDC + str(len(players)) + "/32")                  
            print("-------------------------------------------")
                
        if(self.process_manager.pid_file_running(self.config['server']['pid_file'])):
            print("[{}Yes{}] Server Manager Running".format(bcolors.GREEN, bcolors.ENDC))  
        else:          
            print("[{}No{}] Server Manager Running".format(bcolors.RED, bcolors.ENDC))    
            
        if(self.server_running()):
            print("[{}Yes{}] OpenJK Server Running".format(bcolors.GREEN, bcolors.ENDC))
        else:          
            print("[{}No{}] OpenJK Server Running".format(bcolors.RED, bcolors.ENDC))    
            
        if(self.rtv_running()):
            print("[{}Yes{}] RTV/RTM Service Running".format(bcolors.GREEN, bcolors.ENDC))  
        else:          
            print("[{}No{}] RTV/RTM Service Running".format(bcolors.RED, bcolors.ENDC))    
                
                
        if(self.server_running()):        
                
            print("-------------------------------------------")
            
            print("Players                  Ping ")
            print("-------------------------------------------")                    
            
                    
            if(len(players) > 0):
                    
                for player in players:
                    if(player['ping']):
                        if(int(player['ping']) < 60):
                            ping = bcolors.GREEN + player['ping'] + bcolors.ENDC
 
                        elif(int(player['ping']) < 120):
                            ping = bcolors.YELLOW + player['ping'] + bcolors.ENDC
                        else:
                             ping = bcolors.RED + player['ping'] + bcolors.ENDC
                             
                    print(bcolors().color_convert(player['name']) + "        {}".format(ping) + bcolors.ENDC)
            else: 
                print(bcolors.FAIL + "No one is playing"  + bcolors.ENDC )   

            print("-------------------------------------------")            
                
    # Stop the instance
    def stop(self):
    
        if(self.process_manager.pid_file_running(self.config['server']['pid_file'])):  
            self.process_manager.kill_pid_file(self.config['server']['pid_file'])
            print(bcolors.RED + "Instance is stopping..." + bcolors.ENDC)
        else:
            print(bcolors.RED + "Instance is not running..." + bcolors.ENDC)

    # Stop then start the instance
    def restart(self):     
        self.stop()
        time.sleep(2)
        self.start()           
                        
# Instance manager is used to setup and get instances
class manager:

    # Set Instance name and Get External IP
    def __init__(self):
        self.mbii_manager = mbii_manager(globals.mbii_path)
        
    def get_instance(self, name):
        return server_instance(name)      
        
    def list(self):
        config_file_path = globals.config_path
        for filename in os.listdir(config_file_path):
            if(filename.endswith(".json")):
                print(filename.replace(".json",""))

# Handles Checking Version of MB2, Updating, Downloading, Provisioning



# Main Class
class main:

    manager = None

    # Usage Banner
    def usage(self):
        print("usage: MBII [OPTIONS]")
        print("")
        print("Option                                    Name            Meaning")
        print("-i <instance> [command] [optional args]   Instance        Use to run commands against a named instance")  
        print("-l                                        List            List all Instances available")        
        print("-u                                        Update          Check for MBII Updates, Update when ALL instances are empty")
        print("-v                                        Verbose         Enable verbose mode")          
        print("-h                                        Help            Show this help screen")  
        
        print("")
        
        print("Instance Commands")
        print("Option             Description")
        print("Start              Start Instance")
        print("Stop               Stop Instance") 
        print("Restart            Restart Instance") 
        print("Status             Instance Status") 
        print("rcon               Issue RCON Command In Argument") 
        print("smod               Issue SMOD Command In Argument")         

        
        exit()

    # Main Function
    def main(self,argv):
    
        if(len(sys.argv) == 1):
            self.usage()
            
        self.manager = manager()    
            
        parser = argparse.ArgumentParser(add_help=False)
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-i", type=str, help="Action on Instance", nargs="+", metavar=('INSTANCE', 'ACTION', 'OPTIONAL_ARGS'), dest="instance")   
        group.add_argument("-l", action="store_true", help="List Instances", dest="list")            
        group.add_argument("-u", action="store_true", help="Update MBII", dest="update")    
        group.add_argument("-h", action="store_true", help="Help Usage", dest="help")  
        parser.add_argument("-v", action="store_true", help="Verbosed Output", dest="verbose")   
        
        args = parser.parse_args()
        
        if(args.verbose):
            globals.verbose = True
            
        if(args.help):
            self.usage()
            exit()
            
        if(args.list):
            self.manager.list()
            exit()
                   
        if(args.instance):
        
            if(len(args.instance) == 3):
                getattr(self.manager.get_instance(args.instance[0]), args.instance[1])(args.instance[2])
            elif(len(args.instance) == 4):
                 getattr(self.manager.get_instance(args.instance[0]), args.instance[1])(args.instance[2], args.instance[3])           
            else:
                getattr(self.manager.get_instance(args.instance[0]), args.instance[1])()
        
            #try:
                #getattr(self.manager.get_instance(args.instance[0]), args.instance[1])()
                
            #except:
                #print("Invalid Command " + args.instance[1]) 
        
        elif(args.list): 
            self.manager.list()

        elif(args.update):
            self.manager.update()
        
if __name__ == "__main__":
   main().main(sys.argv[1:])
