

class plugin:

    instance = None

    def __init__(self, instance):
        self.instance = instance
        
    def on_load(self):
        print("loaded RTV Plugin")

    def before_dedicated_server_launch(self):
        print("")
    
    def on_dedicated_server_shutdown(self):
        print("")    