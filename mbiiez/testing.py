
import os
import subprocess
import re

class testing:

    def ping_test(self, host):
    
        try:
            output = subprocess.check_output(['ping', '-c', '4', '-q', host])
            output = output.decode('utf8')
            statistic = re.search(r'(\d+\.\d+/){3}\d+\.\d+', output).group(0)
            avg_time = re.findall(r'\d+\.\d+', statistic)[1]
            response_time = float(avg_time)

        except subprocess.CalledProcessError:
            response_time = 999
      
        return str(response_time)