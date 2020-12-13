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

import random
import datetime

class plugin:

    plugin_name = "Spin Mode"
    plugin_author = "Louis Varley"
    plugin_url = ""

    instance = None
    plugin_config = None
    
    # LIST to hold all previous spins
    spins = {}

    ''' You must initialise instance which you can use to access the running instance '''
    def __init__(self, instance):
        self.instance = instance
        self.config = self.instance.config['plugins']['spin']
        
        if(self.instance.has_plugin("auto_message")):
            self.instance.config['plugins']['auto_message']['messages'].append("You can run the ^3!spin^7 command in chat to get a random perk or handicap")
            self.instance.config['plugins']['auto_message']['messages'].append("^3!spin^7 has a " + str(self.config['cooldown']) + " second cooldown. Use your spins wisley",)
            self.instance.config['plugins']['auto_message']['messages'].append("You can bind spin to a key by opening the console and entering: ^3bind <KEY> 'say !spin'^7")            
            self.instance.config['plugins']['auto_message']['messages'].append("As a Jedi or Sith, you may have to set some keys to allow use of items instead of force powers") 
            self.instance.config['plugins']['auto_message']['messages'].append("Items can only be used by Jedi and Sith when their saber is out... for some reason...") 
            self.instance.config['plugins']['auto_message']['messages'].append("All is fair in Love and Spin! May the luck be with you!")
            
        v = 0    
        for k in self.config['perks_chances']:    
            v = v + self.config['perks_chances'][k] 
            
        if(v > 100 or v < 100):
            self.instance.log_handler.log("Spin Perk Chances is currently {} but should add up to 100%".format(v))

    ''' use register event to have your given method notified when the event occurs '''
    def register(self):
        self.instance.event_handler.register_event("player_chat_command", self.spin_process)
        

        
    def spin_process(self, args):
        if(args['message'].startswith("!spin")): 
        
            rand = random.randint(1,100)
            command = None
            t = 0
            
            if(args['player_id'] in self.spins):
                s = (datetime.datetime.now() - self.spins[args['player_id']]).total_seconds()
                if(s < self.config['cooldown']):
                    self.instance.tell(args['player_id'], "Spin is still in cooldown for another {} seconds".format(int(self.config['cooldown'] - s)))
                    return;
                    
            self.spins[args['player_id']] = datetime.datetime.now()        
    
            for k in self.config['perks_chances']:
                t = t + self.config['perks_chances'][k]
                if(rand <= t):
                    break;
        
            if(k=="lightsaber"): 
                self.instance.tell(args['player_id'], "You win a LightSaber!")    
                command = "wannabe {} give weapon 1".format(args['player_id'])
              
            elif(k=="disruptor"):
                self.instance.tell(args['player_id'], "You win a Disruptor")
                command = "wannabe {} give weapon 4".format(args['player_id']) 
              
            elif(k=="projectile_rifle"): 
                self.instance.tell(args['player_id'], "You win a Projectile Rifle")
                command = "wannabe {} give weapon 5".format(args['player_id'])
                
            elif(k=="bowcaster"):
                self.instance.tell(args['player_id'], "You win a Bowcaster")
                command = "wannabe {} give weapon 6".format(args['player_id'])
                
            elif(k=="dc15"):
                self.instance.tell(args['player_id'], "You win a DC15")
                command = "wannabe {} give weapon 7".format(args['player_id'])
 
            elif(k=="arc_pistol"):
                self.instance.tell(args['player_id'], "You win an ARC Pistol")
                command = "wannabe {} give weapon 8".format(args['player_id'])
                
            elif(k=="rocket_launcher"):
                self.instance.tell(args['player_id'], "You win a Rocket Launcher")
                command = "wannabe {} give weapon 10".format(args['player_id'])               
 
            elif(k=="frag_grenades"):
                self.instance.tell(args['player_id'], "You win a Frag Grenade")
                command = "wannabe {} give weapon 11".format(args['player_id'])               
  
            elif(k=="pulse_grenades"):
                self.instance.tell(args['player_id'], "You win 2 Pulse Grenades")
                command = "wannabe {} give weapon 12".format(args['player_id'])

            elif(k=="t21"):
                self.instance.tell(args['player_id'], "You win a T21")
                command = "wannabe {} give weapon 13".format(args['player_id'])              

            elif(k=="arm_blaster"):
                self.instance.tell(args['player_id'], "You win an Arm Blaster")
                command = "wannabe {} give weapon 14".format(args['player_id'])

            elif(k=="welstar_34"):
                self.instance.tell(args['player_id'], "You win a Welstar34")
                command = "wannabe {} give weapon 14".format(args['player_id'])

            elif(k=="armor_500"):
                self.instance.tell(args['player_id'], "Your armor is now 500")
                command = "wannabe {} give armor 500".format(args['player_id'])
                
            elif(k=="armor_200"):
                self.instance.tell(args['player_id'], "Your armor is now 200")
                command = "wannabe {} give armor 200".format(args['player_id'])                
                
            elif(k=="armor_0"):
                self.instance.tell(args['player_id'], "You armor is now 0")
                command = "wannabe {} give armor 0".format(args['player_id'])

            elif(k=="armor_0"):
                self.instance.tell(args['player_id'], "You armor is now 0")
                command = "wannabe {} give armor 0".format(args['player_id'])
                
            elif(k=="nothing"):
                self.instance.tell(args['player_id'], "You won... nothing, sorry...")
         
            elif(k=="big"):
                command = "wannabe {} set player_scale 150".format(args['player_id'])
                self.instance.tell(args['player_id'], "You unexpectedly grew!")
 
            elif(k=="small"):
                command = "wannabe {} set player_scale 50".format(args['player_id'])
                self.instance.tell(args['player_id'], "Have you lost some weight?")
 
            elif(k=="binovision"):
                command = "wannabe {} set zoom_mode 2".format(args['player_id'])
                self.instance.tell(args['player_id'], "Did you just glue them binoculars to your face?")

            elif(k=="seekerdroid"):
                command = "wannabe {} give item 1".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Padawan's Seekerdroid!")                

            elif(k=="jetpack"):
                command = "wannabe {} give item 7".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Jetpack!")
                
            elif(k=="sentry"):
                command = "wannabe {} give item 6".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Automated Sentry Gun!")                

            elif(k=="cloak"):
                command = "wannabe {} give item 11".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Cloaking Device!")                

            elif(k=="emplacement"):
                command = "wannabe {} give item 10".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Gun Implacement!") 	
         
            elif(k=="bacta"):
                command = "wannabe {} give item 4".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Tank of Bacta!") 	
                  
            elif(k=="forcefield"):
                command = "wannabe {} give item 2".format(args['player_id'])
                self.instance.tell(args['player_id'], "You win a Forcefield Generator!") 
                
            # Log This Spin
            self.spins[args['player_id']] = datetime.datetime.now()
         
            self.instance.rcon(command)
