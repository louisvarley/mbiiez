from mbiiez.models import process
from mbiiez.db import db
from mbiiez.bcolors import bcolors

import multiprocessing
import os

class process_handler:

    instance = None

    def __init__(self, instance):
        self.instance = instance
               
    """ Forks this process, starts the given function and PID to database """               
    def add(self, func, name, instance):

        pid = os.fork()
        if(pid == 0):
            db().insert("processes", {"name": name, "pid": os.getpid(), "instance": instance})
            func()
          
    def process_status(self, name):
        pr = db().select("processes",{"instance": self.instance.name, "name": name})
        
        if(len(pr) == 0):
            return False
        else:
            for p in pr:
                curProcess = process(p)
        
                if(self.is_running(curProcess.pid)):
                    return True
                else:
                    return False
                    
    def stop_all(self):
        pr = db().select("processes",{"instance": self.instance.name})

        if(len(pr) == 0):
            print(bcolors.RED + "Instance not running" + bcolors.ENDC)

        for p in pr:          
            curProcess = process(p)
            if(self.is_running(curProcess.pid)):           
                if(self.stop(curProcess.pid)):               
                    db().delete("processes", curProcess.id)
                    print(bcolors.GREEN + "[Yes]" + bcolors.ENDC +  " Stopped {}".format(str(curProcess.name)))
                else:
                    print(bcolors.RED + "[No]" + bcolors.ENDC +  " Stopped {}".format(str(curProcess.name))) 
            else:
                db().delete("processes", curProcess.id)

        # The above is quite good for keeping track of processes, ultimately it does not work....
        # This is the brute force... burn it all, command
        cmd = "ps aux | grep -ie " + self.instance.name + "- | awk '{print $2}' | xargs kill -15 >/dev/null 2>&1"
        os.system(cmd)                 

    def is_running(self, pid):
        try:
             os.kill(pid, 0)
             return True
             
        except OSError:           
            return False
            
    def stop(self, pid):
    
        try:
             os.kill(pid, 9)
             return True
             
        except OSError:           
            return False    