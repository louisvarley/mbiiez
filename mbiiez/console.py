import time
import six
import re

from socket import (socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, SHUT_RDWR, gethostbyname_ex,
                    gaierror, timeout as socketTimeout, error as socketError)
                    
# Client for Handling RCON, SMOD and RAW server UDP Commands  
class console:

    rcon_password = None
    server_port = None
    header = (chr(255) + chr(255) + chr(255) + chr(255))

    def __init__(self, rcon_password, server_port):
        self.rcon_password = rcon_password
        self.server_port = int(server_port)
      
    # Send Command as RCON Command  
    def rcon(self, command, quiet = False):
    
        reply = None
        
        try:        
            time.sleep(0.6)   
            if(not quiet):
                print("Sent:{}".format(command))
                
            send_command       = (self.header + "rcon {} {}".format(self.rcon_password, command))          
            serverAddressPort   = ("127.0.0.1", self.server_port)
            bufferSize          = 1024
            sock = socket(family=AF_INET, type=SOCK_DGRAM)
            socket.settimeout(sock, 4)           
            sock.sendto(six.b(send_command), serverAddressPort)
            reply = sock.recvfrom(bufferSize)
            reply = reply[0][4:].decode() 
            sock.close()    

            if reply.startswith("print\nbad rconpassword"):
                print("Incorrect rcon password.")               

            elif(reply.startswith("disconnect")):
                print("got a disconnect response")               

            elif not reply.startswith("print"):
                print("Unexpected error while contacting server for the first time.")

            if(not quiet):
                print("Reply:{}".format(reply))
                
            return reply

        except Exception as e:
            print("RCON Error: " + str(e))
            
        finally:
            sock.close()

    # Send Command as CONSOLE command
    def console(self, command, quiet = False):
    
    
        reply = None
    
        try:
            time.sleep(0.6)
            if(not quiet):
                print("Sent:{}".format(command))
                
            send_command       = (self.header + "{}".format(command))
            serverAddressPort   = ("127.0.0.1", self.server_port)
            bufferSize          = 1024
            sock = socket(family=AF_INET, type=SOCK_DGRAM)
            socket.settimeout(sock, 4)   
            sock.sendto(six.b(send_command), serverAddressPort)
            reply = sock.recvfrom(bufferSize)           
            reply = reply[0][4:].decode('utf-8', 'ignore')
            sock.close()
            
            if(reply == None):
                return "No Response"

            elif(reply.startswith("disconnect")):
                print("got a disconnect response")               

            if(not quiet):
                print("Reply:{}".format(reply))
                
            return reply                

        except Exception as e:
            print("Console Error: " + str(e))
            
        finally:
            sock.close()   

    def say(self, message):
        self.rcon("svsay " + message)
        
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
            