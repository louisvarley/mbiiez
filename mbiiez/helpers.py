
import re
import re
import json
import urllib.request

class helpers:

    def ansi_strip(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        text = ansi_escape.sub('', text)
        
        # Change to Regex, CBA At the moment
        text = text.replace("^1", "")
        text = text.replace("^2", "")
        text = text.replace("^3", "")
        text = text.replace("^4", "")
        text = text.replace("^5", "")
        text = text.replace("^6", "")
        text = text.replace("^7", "")
        text = text.replace("^0", "")
        text = text.replace("^9", "")         
        
        if(text == ""):
            text = None

        return text

    def ip_info(self, ip = None):
    
        if(ip == None):
            response = urllib.request.urlopen('http://ipinfo.io/json')
        else:
            response = urllib.request.urlopen("http://ipinfo.io/{}/json".format(ip))
        return json.load(response)
        
    def safe_string(self, text):
        text = text.replace('"','\"')
        return text