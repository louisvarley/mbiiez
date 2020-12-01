
import os, sys, inspect
import importlib
from plugins import *

import importlib
import pkgutil

from mbiiez import settings

 # Info:
 # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
 # __file__ fails if the script is called in different ways on Windows.
 # __file__ fails if someone does os.chdir() before.
 # sys.argv[0] also fails, because it doesn't not always contains the path.

class plugin_handler:

    instance = None
    
    def __init__(self, instance):
        self.instance = instance
        
        sys.path.insert(0, settings.locations.plugins_path)

        discovered_plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith('plugin_')
        }
        
        for p in discovered_plugins:
            plugin = discovered_plugins[p].plugin(self.instance)
            if(hasattr(plugin, 'on_load')):
                plugin.on_load()
        
        #plugins.rtvrtm.rtvrtm.plugin.on_load()
    