import os
import psutil

class process:

    # Return a PID contained in a given file
    def get_pid_from_file(self, pid_file):
        if(os.path.isfile(pid_file)):
            with open(pid_file, 'r') as file:
                pid = file.read()
                
            return int(pid)
        else:
            return 0
            
    # Kill PID contained in a given file
    def kill_pid_file(self, pid_file):
        if(self.pid_file_running(pid_file)):
            pid = self.get_pid_from_file(pid_file)
            try:             
                 os.kill(pid, 15)
                 return True
                 
            except OSError:
                return False
                
    # Is PID in a given file running 
    def pid_file_running(self, pid_file):
        pid = self.get_pid_from_file(pid_file)
        
        if(pid == 0):
            return False
        
        if(self.pid_is_running(pid)):
            return True
        else:
            os.remove(pid_file)     
            return False

    # Is a PID  running
    def pid_is_running(self,pid):
        try:
             os.kill(pid, 0)
             return True
             
        except OSError:           
            return False
                  
    # Return PID of process by name      
    def find_process_by_name(self, search):
        for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            try:
                if(search in p.info["cmdline"]):
                    return p.pid

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return 0
        return 0    
     
    # Kill process by name
    def kill_process_by_name(self, search):
        cmd = "ps aux | grep -ie " + search + " | awk '{print $2}' | xargs kill -15"
        os.system(cmd)   
        
        