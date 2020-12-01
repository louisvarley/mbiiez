#!/usr/bin/python3
import sys, getopt
import argparse

from mbiiez.bcolors import bcolors
from mbiiez.instance import instance
from mbiiez import settings

# Main Class
class main:

    def get_instance(self, name):
        return instance(name)      
        
    def list(self):
        config_file_path = globals.config_path
        for filename in os.listdir(config_file_path):
            if(filename.endswith(".json")):
                print(filename.replace(".json",""))

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
 
        parser = argparse.ArgumentParser(add_help=False)
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-i", type=str, help="Action on Instance", nargs="+", metavar=('INSTANCE', 'ACTION', 'OPTIONAL_ARGS'), dest="instance")   
        group.add_argument("-l", action="store_true", help="List Instances", dest="list")            
        group.add_argument("-u", action="store_true", help="Update MBII", dest="update")    
        group.add_argument("-h", action="store_true", help="Help Usage", dest="help")  
        parser.add_argument("-v", action="store_true", help="Verbosed Output", dest="verbose")   
        
        args = parser.parse_args()
        
        if(args.verbose):
            settings.globals.verbose = True
            
        if(args.help):
            self.usage()
            exit()
            
        if(args.list):
            self.list()
            exit()
                   
        if(args.instance):
        
            if(len(args.instance) == 3):
                getattr(self.get_instance(args.instance[0]), args.instance[1])(args.instance[2])
            elif(len(args.instance) == 4):
                 getattr(self.get_instance(args.instance[0]), args.instance[1])(args.instance[2], args.instance[3])           
            else:
                getattr(self.get_instance(args.instance[0]), args.instance[1])()
      
if __name__ == "__main__":
   main().main(sys.argv[1:])
   print(bcolors.ENDC)
