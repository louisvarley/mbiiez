from mbiiez.bcolors import bcolors
from mbiiez.process import process
import os

class event_handler:

    running = False
    threads = []
    config = None
    log_handler = None
    process = None
    
    def __init__(self, config, log_handler):
        self.config = config
        self.log_handler = log_handler
        self.process = process()
    
    def add_thread(self, thread):
        self.threads.append(thread)
    
    def start(self):
        self.running = True
        
    def stop(self):
        self.running = False
    
    def is_running(self):
        return self.running
        
    def shutdown(self, signal, frame):    
        self.log_handler.log(bcolors.RED + "Gracefull shutdown requested...")
        self.stop()  
        
        # Had trouble ending processes using threads so process brute forces by their config files
        self.process.kill_process_by_name(self.config['server']['server_config_file'])
        self.process.kill_process_by_name(self.config['server']['rtvrtm_config_file'])
        os.system("reset")    
        exit()