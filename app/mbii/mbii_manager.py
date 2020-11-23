class mbii_manager:
    
    _MB2_PATH = None    
        
    def __init__(self, mb2_path):
        self.__MB2_PATH = mb2_path
        
    def get_version(self):
        with open(self.__MB2_PATH + '/version.info', 'r') as file:
            data = file.read().replace('\n', '')
            
        return data
        