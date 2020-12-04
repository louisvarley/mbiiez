''' 
# Instructions
- MBIIEZ Plugins can run actions during certain events. 
- Plugins have access to the full instance and thus can access any data they may need.
- To be enabled on an instance, the plugin must have an entry in the instance config file under plugins.
- Additional settings can be required within the config for your plugin
- Events when raised may send further data you can use as an included dictionary using below arguments. 

# Events

Name                                Arguments                   Description
---------                           ---------                   ---------

before_dedicated_server_launch      None                            Runs before the dedicated server process is started
after_dedicated_server_launch       None                            Runs after the dedicated server process has started

new_log_line                        log_line                        Runs when a new line is added to the log for the instance

 
player_chat_command                 message,player,player_id        When a chat is made with a ! prefix
player_chat                         type, message,player,player_id  When any chat is made

player_connects                     player,player_id                When a new player joins the game
player_disconnects                  player,player_id                When a player disconnects from the game
player_killed                       fragger,fragged,weapon          When a player is killed
player_begin                        player,player_id                When a player starts in a new round

map_change                          map_name                        When the server changes map



'''

import datetime
import os
import discord
import re
import shlex
import threading
import signal
import socket
import time
import prettytable

from discord.ext import commands
from mbiiez.helpers import helpers

class plugin:

    plugin_name = "Discord Bot"
    plugin_author = "Louis Varley"
    plugin_url = ""

    instance = None
    plugin_config = None
    discord_bot = None

    ''' You must initialise instance which you can use to access the running instance '''
    def __init__(self, instance):
        self.instance = instance
        self.config = self.instance.config['plugins']['discord_bot']      
        self.discord_bot = commands.Bot(command_prefix=self.config['command_prefix'], help_command=None)
        self.discord_bot.add_cog(server_bot(self.discord_bot, self.instance))

    ''' use register event to have your given method notified when the event occurs '''
    def register_events(self):
        #self.instance.event_handler.register_event("player_chat_command", self.spin_process)
        self.instance.launcher.register_service("Discord Bot Service", self.start_bot)
        
    def start_bot(self):
        self.discord_bot.run(self.config['token'])

class server_bot_response:

    message = ""

    def append(self, message):
        self.message = self.message + str(message) + "\n"
        
    def get(self):
        return helpers().ansi_strip(self.message)
        
    def clear(self):
        self.message = ""
        
    def empty(self):
        if(len(self.message.strip) == 0):
            return True
        else:
            return False
                    
class server_bot(commands.Cog):
    
    bot = None
    instance = None
    rs = None
    
    def __init__(self, bot, instance):
        self.bot = bot 
        self.instance = instance
        self.rs = server_bot_response()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='Powered By MBIIEZ'))        
            
    ''' So the format is [PREFIX] [INSTANCE] [COMMANDS] only a single command is used here'''
    @commands.command(name="server")
    async def commands_all(self, ctx, *args):
        
        # On list, just says its name, so all bots print their names
        if(args[0] == "list"): 
            self.rs.append("{}".format(self.instance.name))
            await ctx.send(self.rs.get())
        
        # Used if the given instance is not this one, just exit so another bot can deal with request
        if(not args[0] == self.instance.name):
            return
        
        self.rs.clear()

        if(args[1] == "players"):  
            self.rs.append("{} server currently has {} players".format(self.instance.name, self.instance.players_count()))
            
            if(self.instance.players_count() > 0):
                players = self.instance.players()
                if(len(players) > 0):
                    for player in players:
                        self.rs.append(players['name'])

        if(args[1] == "status"):                         
            self.rs.append(os.popen("mbii -i {} status".format(self.instance.name)).read())
            
        if(args[1] == "restart"): 
            self.rs.append("Restarting {}".format(self.instance.name))
            await ctx.send(self.rs.get()) ## Add as once we called restart, we wont get to send
            self.rs.append(os.popen("mbii -i {} restart".format(self.instance.name)))
        
        if(args[1] == "map"):                         
            self.rs.append(os.popen("mbii -i {} map {}".format(self.instance.name, args[2])).read())
                    
        if(not self.rs.empty):
            await ctx.send(self.rs.get())    
