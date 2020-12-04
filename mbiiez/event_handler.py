from mbiiez.bcolors import bcolors
from mbiiez.process import process
import os

class event_handler:

    instance = None

    events = {}

    def __init__(self, instance):
        self.instance = instance
    
    def register_event(self, event_name, func):
        if(not event_name in self.events):
            self.events[event_name] = []
        
        self.events[event_name].append(func)
        
    def run_event(self, event_name, args = None):
        self.instance.log_handler.log("Event {} started".format(event_name))
        if(event_name in self.events):
            for event in self.events[event_name]:
                try: 
                    if(args == None):
                        event()
                    else:
                        event(args)
                except Exception as e:
                    self.instance.log_handler.log("Plugin Exception: {}".format(str(e)))
            