
import re
import re
import json
import urllib.request

class helpers:

    def cvar_clean(self, text):
        return re.sub("\^[1-9]","",text)

    def fix_line(self, line):

      startswith = str.startswith
      split = str.split
      
      # Remove Any Spaces inside peoples usernames
      line = re.sub(r'\(.*?\)', lambda x: ''.join(x.group(0).split()), line)

      while startswith(line[8:], "Client "):

        line = split(line, ":", 3)

        if len(line) < 4: # If this bug is ever fixed within the MBII code,
                          # make sure this fix is not processed.
          return ""

        line[0] = int(line[0]) # Timestamp.

        for i in xrange(-1, -7, -1):

          substring = int(line[-2][i:])

          if (substring - line[0]) >= 0 or line[-2][(i-1)] == " ":

            line = "%3i:%s" % (substring, line[-1])
            break

      return line
      
    def ansi_strip(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', text)
        if(result == ""):
            result = None

        return result

    def ip_info(self, ip = None):
    
        if(ip == None):
            response = urllib.request.urlopen('http://ipinfo.io/json')
        else:
            response = urllib.request.urlopen("http://ipinfo.io/{}/json".format(ip))
        return json.load(response)