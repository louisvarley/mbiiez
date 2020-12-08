from mbiiez.models import process
from mbiiez.db import db
from mbiiez.bcolors import bcolors

import multiprocessing
import os
import time
import subprocess
import shlex

class process_handler:

    instance = None
    services = []
    
    def __init__(self, instance):
        self.instance = instance
               
    def register_service(self, name, func, priority = 99, awaiter = None):
        """ 
            Register a function as a service. Runs as a fork with PIDs stored in database
        """
        self.services.append({"name": name, "func": func, "priority": priority, "awaiter": awaiter})

    def launch_services(self):
        """ 
            Launch all services 
        """       
        # Sort by Priority
        services = sorted(self.services, key=lambda k: k['priority'])
        
        for service in services:
        
            if(service['awaiter'] and callable(service['awaiter'])):
                service['awaiter']();
        
            self.instance.log_handler.log("Starting Service: " + service['name'])
            print(bcolors.OK + "[Yes] " + bcolors.ENDC + "Launching " + service['name'])   
            self.start(service['func'], service['name'], self.instance.name)
            time.sleep(1)
            
    def start(self, func, name, instance):
        """ 
            Start a given func (or shell command), with name for instance 
        """         
        if(callable(func)):
        
            pid = os.fork()
            if(pid == 0):
            
                # Capture the PID for this fork
                db().insert("processes", {"name": name, "pid": os.getpid(), "instance": instance})

                times_started = 0

                # Begin a Loop
                while(True):
                
                    self.instance.log_handler.log("Starting Service: {}".format(name))
                
                    if(times_started > 10):
                        self.instance.log_handler.log("{} Failed to start after 10 tries".format(name))
                        break;
                     
                    try:
                         func()
                    except Exception as e:     
                        self.instance.log_handler.log("{} Crashed with exception {}".format(name, str(e)))
                         
                    # Reached is func ends, should not end    
                    times_started = times_started + 1
                    time.sleep(1)
                          
        # Shell command called, run as shell command
        else:

            std_out_file = "/var/log/{}-{}-output.log".format(instance.lower(),name.lower())

            # Used to clear the file, these output looks are not for persistant logging
            open(std_out_file, 'w').close()

            pid = os.fork()
            if(pid == 0):
            
                func = "{} ".format(func)
                
                container_name = name + " Container"
            
                # When running a shell command, a fork is created which acts are the parent to the new process.
            
                db().insert("processes", {"name": container_name, "pid": os.getpid(), "instance": instance})
                
                self.instance.log_handler.log("Starting Service: {}".format(name))

                process = None
                crashes = 0
                
                # Begin Loop
                while(True):
                
                    # Should stop this process if requested to stop
                    if(not self.process_status(container_name)):
                        break;
                        
                    if(crashes > 10):
                        self.instance.log_handler.log("Service: {} was unable to start after 10 retries...".format(name))
                        print("Crashed too many times")
                        break;
                        
                    # Start the Process
                    if(process == None):  
                        log = open(std_out_file, 'a')
                        process = subprocess.Popen(shlex.split(func), shell=False, stdin=log, stdout=log, stderr=log) 
                        db().insert("processes", {"name": name, "pid": process.pid, "instance": instance})            

                    # If either POLL returns some error or the PID is not running at all
                    if(not process == None):     
                        if(not process.poll() == None or not self.process_status(name)): # WHEN PROCESS CRASHES, POLL AND STATUS STILL SHOW ACTIVE
                            print("process {} crashed".format(name))
                            crashes = crashes + 1
                            self.stop(process.pid)                     
                            db().delete("processes", process.pid)  
                            process = None
                            self.instance.log_handler.log("Restarting Service: {}".format(name))

                    time.sleep(3)

    def process_status(self, name):
        """ 
            Is a given process by name running?
        """       
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