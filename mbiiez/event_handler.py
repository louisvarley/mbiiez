from mbiiez.bcolors import bcolors
from mbiiez.process import process
from mbiiez.db import db
import os
import datetime
import time

class event_handler:

    instance = None

    events = {}

    def __init__(self, instance):
        self.instance = instance
    
    def register_event(self, event_name, func):
        if(not event_name in self.events):
            self.events[event_name] = []
        
        self.events[event_name].append(func)
        
    def run_event(self, event_name, args = None):

        if(event_name in self.events):
            for event in self.events[event_name]:
                try: 
                    if(args == None):
                        event()
                    else:
                        event(args)
                except Exception as e:
                    self.instance.exception_handler.log(e)

    # Designed to allow server to restart after a given number of hours automatically providing its empty
    def restarter(self):
        
        restart_hours = self.instance.config['server']['restart_instance_every_hours']
        
        while(True):
            self.instance.log_handler.log("Next Scheduled Restart will be at ")
            time.sleep(restart_hours * 60 * 60)
            self.instance.log_handler.log("Attempting Scheduled Restart")
            
            # If Server is not empty when due to restart, then check every minute
            while(not self.instance.is_empty()):
                self.instance.log_handler.log("Server not empty, restart postponed..")
                time.sleep(600)
                
            # Does the restart    
            os.popen("mbii -i {} restart".format(self.instance.name))    
        

    # Internal Events
    # These are methods used by MBII to record internal events

    def player_chat_command(self, args):
        return
    
    def player_chat(self, args):
        d = {"added": str(datetime.datetime.now()), "player":args['player'], "instance": self.instance.name, "type": "PUBLIC", "message": args['message']}
        return db().insert("chatter", d)    
        
    def player_chat_team(self, args):
        d = {"added": str(datetime.datetime.now()), "player":args['player'], "instance": self.instance.name, "type": "TEAM", "message": args['message']}
        return db().insert("chatter", d)    
    
    def player_killed (self, args):
        d = {"added": str(datetime.datetime.now()), "instance": self.instance.name, "fragger": args['fragger'], "fragged": args['fragged'], "weapon": args['weapon']}
        return db().insert("frags", d)
        
    def player_connected (self, args):    
        d = {"added": str(datetime.datetime.now()), "player": args['player'], "player_id": args['player_id'], "instance": self.instance.name, "ip": args['ip'], "type": "CONNECT"}
        return db().insert("connections", d)
    
    def player_disconnected (self, args):  
        d = {"added": str(datetime.datetime.now()), "player": args['player'], "player_id": args['player_id'], "instance": self.instance.name, "ip": args['ip'], "type": "DISCONNECT"}
        return db().insert("connections", d)

    def player_begin (self, args):
        return 
        
    def player_info_change(self, args):
    
        game_classes = [
            "None",
            "Storm Trooper",
            "Solder",
            "Commander",
            "Elite Solder",
            "Sith",
            "Jedi",
            "Bounty Hunter",
            "Hero",
            "Super Battle Droid",
            "Wookie",
            "Deka",
            "Clone",
            "Mando",
            "Arc Trooper"
        ]    
    
        line = args['data']
        info_split = line.split("\\")
        
        player_id = line.split(" ")[2]
        player = info_split[1]
        model = info_split[5]
        class_id = int(info_split[19])
        class_name = game_classes[class_id]
 
        d = {"added": str(datetime.datetime.now()), "player": player, "player_id": player_id, "instance": self.instance.name, "class_name": class_name, "class_id": class_id, "model": model}
        return db().insert("player_info", d)    
      
                