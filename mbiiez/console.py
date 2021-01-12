import time
import six
import re
import socket 

class console:

    def __init__(self, rcon_password, server_port):
        self.ip = "127.0.0.1"
        self.port = int(server_port)
        self.password = rcon_password
        self.prefix_rcon = bytes([0xff, 0xff, 0xff, 0xff]) + b'rcon '
        self.prefix_console = bytes([0xff, 0xff, 0xff, 0xff])        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def rcon(self, command, quiet = False):
        cmd = f"{self.password} {command}".encode()
        query = self.prefix_rcon + cmd
        return self.send(query)

    def console(self, command, quiet = False):
        cmd = f"{command}".encode()
        query = self.prefix_console + cmd    
        return self.send(query)

    def send(self, query):
        self.socket.connect((self.ip, self.port))
        self.socket.send(query)
        socket.socket.settimeout(self.socket, 4)    
        
        try:
            data = self.socket.recv(4096)
            data = data.decode("utf-8", "ignore")
       
            return data
        except socket.timeout:
            return None

    # Send SAY as Server
    def say(self, message):
        self.rcon("svsay {}".format(message))
       
    # Send TELL as server (To Player)   
    def tell(self, player_id, message):
        self.rcon("svtell {} {}".format(player_id,message))
        
    def cvar(self, key, value = None):
    
        if(value == None): # GET a CVAR Value
            response = self.rcon(key, True)
            try:
                #OpenJK
                if("cvar" in response.lower()):
                    response = re.findall(r'"([^"]*)"', response)[0]               
                #JAMP    
                else:
                    response = response.split('"')[1::2][1]; # the [1::2] is a slicing which extracts odd values                
            except:    
                print("Error, unknown or invalid cvar")
                
            result = self.cvar_clean(response)   
            return result
        
        else: #SET a CVAR Value
            response = self.rcon("set " + key + "=" + str(value))             
            
    def cvar_clean(self, text):
        return re.sub("\^[1-9]","",text)
   
 