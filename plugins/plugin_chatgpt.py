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
import openai  # Make sure to install the openai library (pip install openai)


from mbiiez.client import client

class plugin:

    plugin_name = "ChatGPT"
    plugin_author = "Louis Varley"
    plugin_url = ""

    instance = None
    plugin_config = None

    ''' You must initialise instance which you can use to access the running instance '''
    def __init__(self, instance):
        self.instance = instance
        self.config = self.instance.config['plugins']['chatgpt']
     
        #OpenAPI API Key
        openai.api_key = self.config['apikey']
        
        self.process_bot_instructions()
        
        if(self.instance.has_plugin("auto_message")):
            self.instance.config['plugins']['auto_message']['messages'].append("This server has DAVE the AI overlord available, talk to him directly with !dave")   
            
    ''' use register event to have your given method notified when the event occurs '''
    def register(self):
        self.instance.event_handler.register_event("player_chat_command", self.on_chat)
        self.instance.event_handler.register_event("player_killed", self.on_killed)       
        self.instance.event_handler.register_event("player_begin", self.on_begin)  
        self.instance.event_handler.register_event("player_disconnects", selfon_disconnectstats_process)  
          
    def on_chat(self,args):
        player = args['player']
        type = args['type'] #TEAM or PUBLIC
        message = args['message']    

        if message.startswith('!dave'):
            response = self.generate_chat_response(f"{player}! said the following to you directly chatgpt: {message}")
            self.say(response)  
        else:
            response = self.generate_chat_response(f"{player}! said the following, but it was not said to you: {message}")
            self.say(response)         
    
    def on_killed(self,args):
        fragger = args['fragger']
        fragged = args['fragged']
        weapon = args['weapon']
        # Create a kill announcement using ChatGPT
        announcement = self.generate_kill_announcement(fragger, fragged, weapon)
        self.say(announcement)         
          
    def on_begin(self,args):
         player = args['player']
         
    def on_disconnect(self,args):
         player = args['player']
    
    # Tell a player, no one else will see the message
    def tell(player_id, message):
        self.instance.tell(player_id, message)
    
    def generate_chat_response(self, input_text):
        # Use ChatGPT to generate a response to player chat commands
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=input_text,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def generate_kill_announcement(self, fragger, fragged, weapon):
        # Use ChatGPT to generate a kill announcement
        announcement = f"{fragger} takes down {fragged} with a {weapon}! Impressive marksmanship!"
        return self.generate_chat_response(announcement)

    def say(self, message):
        my_client = client(player)
        my_client.send_message(message)
        
    def process_bot_instructions(self):

        instructions = """
        Instructions for ChatGPT Movie Battles 2 Plugin

        1. **Selective Chat Engagement:**
           - Respond to in-game chat messages selectively.
           - Consider responding to keywords like "help," "tips," or specific in-game events.
           - Avoid responding to every message to maintain a balanced experience.

        2. **Kill Announcements:**
           - Announce notable kills or streaks in a creative and engaging manner.
           - Add flair to kill announcements to enhance the in-game experience.

        3. **Top Fragger Recognition:**
           - Periodically announce the current top fragger or congratulate players on high kill counts.
           - Encourage friendly competition among players.

        4. **Weapon Challenges:**
           - Initiate challenges based on weapon usage to encourage players to diversify their loadouts.
           - Acknowledge players who excel with specific weapons.

        5. **Personalized Announcements:**
           - Personalize kill announcements based on player history or achievements.
           - Use player names and context to make responses more engaging.

        6. **Interactive Conversations:**
           - Engage in text-based conversations with players who initiate interactions.
           - Provide tips, advice, or add a touch of humor to enhance player engagement.

        7. **Event Triggers:**
           - Trigger special in-game events or announcements based on specific keywords or phrases.
           - Create surprises or challenges for players at opportune moments.

        8. **Balanced Interaction:**
           - Aim for a balanced and enjoyable interaction with players.
           - Avoid overwhelming the chat with too many responses.

        9. **Adaptability:**
           - Be adaptable to different in-game situations.
           - Adjust responses based on the context of the chat or kill events.

        10. **Privacy and Security:**
            - Prioritize player privacy and security.
            - Avoid revealing sensitive information or engaging in inappropriate conversations.

        Remember, the goal is to enhance the overall gaming experience and create a dynamic and engaging atmosphere for players. 
        Feel free to adapt these instructions as needed.
        """
        
        response = openai.Completion.create(
                   engine="text-davinci-002",
                   prompt=instructions,
                   temperature=0.7,
                   max_tokens=150
               )
