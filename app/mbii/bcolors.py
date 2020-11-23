# Static Class to hold Some Random Colours                        
class bcolors:

    #^1 - red 
    #^2 - green 
    #^3 - yellow 
    #^4 - blue 
    #^5 - cyan 
    #^6 - purple 
    #^7 - white 
    #^0 - black 
    #^9 - blank

    HEADER = '\033[95m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    PURPLE = '\033[35m'
    WHITE = '\033[0m'
    BLACK = '\033[0m'
    
    T = "123"
    
    def color_convert(self, text):
    
        text = text.replace("^1", self.RED)
        text = text.replace("^2", self.GREEN)
        text = text.replace("^3", self.YELLOW)
        text = text.replace("^4", self.BLUE)
        text = text.replace("^5", self.CYAN)
        text = text.replace("^6", self.PURPLE)
        text = text.replace("^7", self.WHITE)
        text = text.replace("^0", self.BLACK)
        text = text.replace("^9", "")        
        return text
        