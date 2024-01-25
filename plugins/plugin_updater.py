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
import time
import hashlib
import requests
import xml.etree.ElementTree as ET
import base64

class plugin:

    plugin_name = "MB2 Updater"
    plugin_author = "Louis Varley"
    plugin_url = ""

    instance = None
    plugin_config = None
    discord_bot = None

    ''' You must initialise instance which you can use to access the running instance '''
    def __init__(self, instance):
        self.instance = instance
        self.config = self.instance.config['plugins']['updater']
        self.openjkPath = self.instance.config['server']['openjk_path']

    ''' use register event to have your given method notified when the event occurs '''
    def register(self):
        self.instance.process_handler.register_service("Movie Battles 2 Update Service", self.updater)
        
      # Auto Map Changes Thread       
    def updater(self):             
    
        time.sleep(3)
        updated = False
    
        while(True):
            time.sleep(self.config['check_for_updates_every_minutes'] * 60)
            if(self.instance.is_empty()):

                # Download the Manifest XML file
                xml_url = 'http://update.moviebattles.org/MB2Core.xml'
                response = requests.get(xml_url)
                xml_data = response.content

                # Parse the XML
                root = ET.fromstring(xml_data)

                # Directory where your files are stored (adjust as necessary)
                local_directory = self.openjkPath
                
                print("searching for updates " + local_directory)
   
                for patch_record in root.findall('.//PatchRecord'):
                    file_name = patch_record.find('FileName').text.lstrip('/')  # Remove leading slash
                    
                    if("mbii.x86.app" in file_name):  
                        continue
                    
                    local_file_path = os.path.join(local_directory, file_name)

                    if os.path.exists(local_file_path):
                    
                        expected_hash = patch_record.find('FileHash').text
                        local_hash = self.calculate_hash(local_file_path)
                
 
                        if local_hash != expected_hash:
                            print(f"Updating file: {file_name}")

                            # Define the URL for downloading the file
                            download_url = f'http://update.moviebattles.org/files/{file_name}'
                            self.download_file(download_url, local_file_path)  

                            updated = True
                                               
                    else:
                         download_url = f'http://update.moviebattles.org/files/{file_name}'
                         self.download_file(download_url, local_file_path)                     
                         updated = True

                    if(updated):
                        updated = False
                        self.instance.restart


        return
       

    # Function to download file
    def download_file(self, url, filename):
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def calculate_hash(self, filename):
        try:
            hasher = hashlib.sha256()
            with open(filename, 'rb') as file:
                buf = file.read()
                hasher.update(buf)
            return base64.b64encode(hasher.digest()).decode()
        except Exception as e:
            print(f"Error calculating hash for file {filename}: {e}")
            return None
