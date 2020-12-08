"""
Log Handler: Handles logging, reading from log file and logging to database

Requires: An Instance

"""

import datetime
import tailer
import time
import re
import os
import random
from mbiiez.helpers import helpers

from mbiiez.models import chatter, log, frag, connection


class log_handler:
    
    instance = None

    def __init__(self, instance):
        self.instance = instance
        self.log_file = self.instance.config['server']['log_path']


    def log_await(self):
        x = 0
        
        SECONDS_TO_WAIT = 10
        MAX = (SECONDS_TO_WAIT * 2)
        
        while(not os.path.exists(self.instance.config['server']['log_path']) or x >= MAX): 
            time.sleep(0.5)
            x = x + 1        
        
        if(x >= MAX):
            raise Exception('Dedicated server did not create a log file within 10 seconds')
        else:
            return True


    def log_watcher(self):
        """
        Watches the log file for this instance, and sends lines to be processed
        """   
        self.log_await()
            
        for line in tailer.follow(open(self.instance.config['server']['log_path'])):
                self.instance.log_handler.process(line)


    def log_line_count(self):
        """
        Count the current # of lines in the instances log file
        """    
        f = open(self.log_file, 'rb')
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.raw.read

        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b'\n')
            buf = read_f(buf_size)

        return lines


    def log(self, log_line):
        """
        log to database
        """    
        log_line = log_line.lstrip().lstrip()
        log_line = helpers().ansi_strip(log_line)
        log().new(log_line, self.instance.name)
        
    def process(self, last_line):
        """
        Processes a log line in the log file
        """   
        try:
        
            self.log(last_line)
            
            # Was a chat
            if('say:' in last_line):
                player = last_line.split(":")[3].strip()
                message = last_line.split(":")[4].strip()[1:-1]
                player_id = connection().get_player_id_from_name(player)

                # Run command event
                if(message.startswith("!")):                 
                    self.instance.event_handler.run_event("player_chat_command",{"message": message, "player_id": player_id, "player": player})
                     
                else:     
                     
                    # Run chat event     
                    self.instance.event_handler.run_event("player_chat",{"type": "PUBLIC", "message": message, "player_id": player_id, "player": player})  
                    
                    # Save to Database
                    chatter().new(player, self.instance.name, "PUBLIC", message)
            

            if('sayteam:' in last_line):
                player = last_line.split(":")[3].strip().lstrip()
                message = last_line.split(":")[4].strip()[1:-1]
                player_id = connection().get_player_id_from_name(player)
                
                # Run chat event     
                self.instance.event_handler.run_event("player_chat",{"type": "TEAM", "message": message, "player_id": player_id, "player": player})  

                # Save to Database                
                chatter().new(player, self.instance.name, "TEAM", message)            
            
                
            if('Kill:' in last_line):
                frag_info = last_line.split(":")[3]
                weapon = frag_info.split(" by ")[1]
                players = frag_info.split(" by ")[0]
                fragger = players.split(" killed ")[0].lstrip()
                fragged = players.split(" killed ")[1].rstrip()
                
                if(fragger == fragged or "<world>" in fragger):
                    fragger = "SELF"

                frag().new(self.instance.name, fragger, fragged, weapon)   

            if('ClientConnect:' in last_line):
                player = last_line.split(":")[2][:-4][1:].lstrip().lstrip("(")
                player_id = last_line.split(":")[3][:-4][1:].lstrip()
                ip = last_line.split(":")[4][1:]
                type = "CONNECT"
                connection().new(player, player_id, self.instance.name, ip, type)     

            if('ClientDisconnect:' in last_line):
                player = ""
                player_id = last_line.split(":")[2][1:]
                ip = ""
                type = "DISCONNECT"
                connection().new(player, player_id, self.instance.name, ip, type)  
                
            if('ClientBegin:' in last_line):
                player = ""
                player_id = last_line.split(":")[2][1:]                
                self.instance.event_handler.run_event("player_begin",{"player_id": player_id, "player": player})  

        except Exception as e:
            self.instance.exception_handler.log(e)

            #28:45 ClientConnect: (^3|NR|^7476) ID: 0 (IP: 73.199.53.19:29070)
            #Send Player Connected
            
            # 0  1                   2        
            #28:45 ClientDisconnect: 0
            #Send Player Disconnected  
                        
            #21:04 : say: ^3|NR|^5SEAL^7TeamRicks: "!report something something"
            #Send Moderator Report
            
            #21:04 Kill: 0 7 86: ^3|NR|^7476 killed |^3NR^7|DIO|^3PFC by MOD_SABER
            #Send a Kill
