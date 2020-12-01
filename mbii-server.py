#!/usr/bin/python3

import json
import os
import glob
import shutil
import psutil
import subprocess
import time
import threading
import watchgod
import signal
import six
import sys
import datetime

from mbiiez.bcolors import bcolors
from mbiiez.helpers import helpers
from mbiiez.testing import testing
from mbiiez.instance import instance
from mbiiez.conf import conf
from mbiiez.process import process
from mbiiez.console import console
from mbiiez.db import db
from mbiiez import settings
from mbiiez.launcher import launcher


class main:

    launcher = None

    def start(self, name):
    
        self.instance = instance(name)
        self.launcher = launcher(self.instance)
        
        #print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)   
        #print(bcolors.GREEN + "Starting Server Instance..." + bcolors.ENDC)
        #print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)   

        self.instance.log_handler.log("Starting server instance...")
        self.launcher.launch_auto_message()
        self.launcher.launch_rtv()
        self.launcher.launch_game()
        self.launcher.launch_log_watch()

        #print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)   
        #print(bcolors.GREEN + "Ctrl + C to exit..." + bcolors.ENDC)
        #print(bcolors.GREEN + "---------------------------" + bcolors.ENDC)    
        
        #signal.signal(signal.SIGINT, self.event_handler.shutdown)
        #signal.signal(signal.SIGTERM, self.event_handler.shutdown)

        print("done")
        
if __name__ == "__main__":

    name = sys.argv[1]
    if(name == None):    
        print("Usage: mbii-server *INSTANCE*")
        
    main().start(name)
           
