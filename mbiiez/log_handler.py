"""
Log Handler: Handles logging, reading from log file and logging to database

Requires: An Instance

"""

import datetime
import tailer
import re
import random
from mbiiez.helpers import helpers

from mbiiez.models import chatter, log, frag, connection


class log_handler:
    
    instance = None

    def __init__(self, instance):
        self.instance = instance
        self.log_file = self.instance.config['server']['log_path']

    """
    Watches the log file for this instance, and sends lines to be processed
    """
    def log_watcher(self):
        for line in tailer.follow(open(self.instance.config['server']['log_path'])):
                self.instance.log_handler.process(line)

    """
    Count the current # of lines in the instances log file
    """
    def log_line_count(self):
        f = open(self.log_file, 'rb')
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.raw.read

        buf = read_f(buf_size)
        while buf:
            lines += buf.count(b'\n')
            buf = read_f(buf_size)

        return lines

    """
    log to database
    """
    def log(self, log_line):
        log_line = log_line.lstrip().lstrip()
        log_line = helpers().ansi_strip(log_line)
        log().new(log_line, self.instance.name)
        
    """
    Processes a log line in the log file
    """ 
    def process(self, last_line):
  
        try:
        
            self.log(last_line)
                   
            if('!hello' in last_line):
                quotes = ['Hello There', 'You want to go home and rethink your life', 'These are ^1not^7 the droids you are looking for', 'So uncivilized', 'How did this happen? We\'re smarter than than', 'Another happy landing', 'If you strike me down, i shall become more powerful than you can possibly imagine', 'I have the high ground', '^1Don\'t^7 try it!', '^2Sith^7 lords are our speciality']
                quote = random.choice(quotes)
                self.instance.say(quote)
                
            if('!stats' in last_line):    
                player = last_line.split(":")[3].lstrip()
                response = frag().get_kd(player)
                self.instance.say("{}, your NR Server KD is".format(player))
                self.instance.say("^5Kills:^7" + str(response['kills']))
                self.instance.say("^5Deaths:^7" + str(response['deaths']))
                self.instance.say("^5Suicides:^7" + str(response['suicides']))

            if('!playwithme' in last_line):
                self.instance.say("We will announce your presense in our discord")

            if('!help' in last_line):
                self.instance.say("^5Available Commands^7")
                self.instance.say("^5!hello^7 Random Obi Wan Quote")                
                self.instance.say("^5!stats^7 Your global stats from our servers")     
                self.instance.say("^5!lastonline^7 When was you last on our servers?")   
                self.instance.say("^5!report <message>^7 Send a report to our mods") 
                
            if('say:' in last_line):
                player = last_line.split(":")[3].lstrip()
                message = last_line.split(":")[4]
                chatter().new(player, self.instance.name, "PUBLIC", message)

            if('sayteam:' in last_line):
                player = last_line.split(":")[3].lstrip()
                message = last_line.split(":")[4]
                chatter().new(player, self.instance.name, "TEAM", message)
                
            if('!spin' in last_line):
                if(not self.instance.config['server']['enable_spin']):
                    self.instance.say("^5!" + player + "^7 Spin is not enabled on this server") 
                else:
                    player_id = None
                    player = last_line.split(":")[3].lstrip()
                    self.instance.say("^5!" + player + "^7 Requested a spin") 
                    
                    results = connection().get_player_id_from_name(player)
                    for result in results:
                    
                        player_id = result['player_id']
                     
                    if(player_id == None):
                        self.instance.say("^5!" + player + "^7 Something went wrong! Sorry :(") 
                    else:
                        # Random Number
                        rand = random.randint(1,16)
                        
                        if(rand == 16):
                            command = "wannabe {} give jetpack".format(player_id)
                            self.instance.say("^5!" + player + "^7 Won a new shiny jetpack") 
                        else:
                            if(rand == 1):
                                self.instance.say("^5!" + player + "^7 Won a ") 
  
                            if(rand == 2):
                                self.instance.say("^5!" + player + "^7 Won a Light Saber") 
                                
                            if(rand == 3):
                                self.instance.say("^5!" + player + "^7 Won a Pistol...") 
                            if(rand == 4):
                                self.instance.say("^5!" + player + "^7 Won a E11... Sorry it has no Ammo") 
                            if(rand == 5):
                                self.instance.say("^5!" + player + "^7 Won a Disruptor, go get em champ!") 
                            if(rand == 6):
                                self.instance.say("^5!" + player + "^7 Won a Projectile Rile, enjoy!") 
                            if(rand == 7):
                                self.instance.say("^5!" + player + "^7 Won a Bowcaster! Be a wookie!") 
                            if(rand == 8):
                                self.instance.say("^5!" + player + "^7 Won a DEMP Pistol, go be an ARC!") 
                            if(rand == 9):
                                self.instance.say("^5!" + player + "^7 Won a DC15.. pip pip")                                 
                            if(rand == 10):
                                self.instance.say("^5!" + player + "^7 Won a Rocket Launcher! Oowho Baby!") 
                            if(rand == 11):
                                self.instance.say("^5!" + player + "^7 Won 2 Frag Grenades, make em count") 
                            if(rand == 12):
                                self.instance.say("^5!" + player + "^7 Won 2 Pulse Grenades, go fry some droids ") 
                            if(rand == 13):
                                self.instance.say("^5!" + player + "^7 Won a T21, without alterntate fire enabled... have fun with that") 
                            if(rand == 14):
                                self.instance.say("^5!" + player + "^7 Won an arm blaster... loving stuck onto your arm ") 
                            if(rand == 15):
                                self.instance.say("^5!" + player + "^7 Won a Welstar pistol! no go be a mando!")   
                                
                            command = "wannabe {} give weapon {}".format(result['player_id'], str(rand))
                        
                        self.instance.rcon(command)
                
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
