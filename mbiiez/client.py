from mbiiez.db import db
from mbiiez.helpers import helpers
from mbiiez.bcolors import bcolors

class classes:

    game_classes = [
        "None",
        "Storm Trooper",
        "Solder",
        "Commander",
        "Elite Solder",
        "Sith",
        "Jedi",
        "Bounty Hunter",
        "Hero",
        "Super Battle Droid",
        "Wookie",
        "Deka",
        "Clone",
        "Mando",
        "Arc Trooper"
    ]

class global_stats:
    '''
    Global Stats Across ALL Servers
    '''
    kills = None # Global Kills
    deaths = None # Global Deaths
    suicides = None # Global Suicides
    play_time = None # Global Play Time
    
class game_stats:
    '''
    Stats from their LAST played game on any server
    '''
    player_id = None
    player = None 
    model = None
    class_id = None 
    class_name = None
    instance = None
    last_played = None
    
class client:

    global_stats = None
    game_stats = None

    def __init__(self, player_name):
        '''
        Initialised by asking for details of a given player by name
        '''
        player_name = helpers().ansi_strip(player_name)     
        self.get_client_by_name(player_name)
    
    def get_client_by_name(self, player_name):
        '''
        Fetches the LATEST connection for the given player name
        '''
        conn = db().connect()
        cur = conn.cursor()
        player_name = helpers().ansi_strip(player_name)     
        q = ''' SELECT * FROM connections where player LIKE "%''' + player_name + '''%" AND type = "CONNECT" ORDER BY added DESC LIMIT 1; '''

        cur.execute(q)
        result = cur.fetchone()

        if(result == None):
            return None
        
        player_name = result['player']
        player_id = result['player_id'] # Latest player_id they had
        instance = result['instance'] # Latest instance they played

        self.game_stats = self.get_game_stats(instance, player_name)
        self.global_stats = self.get_global_stats(player_name)

    def get_global_stats(self, player_name):
        stats = global_stats()
        
        conn = db().connect()
        cur = conn.cursor()
        
        kills = 0
        deaths = 0
        suicides = 0
        
        player_name = helpers().ansi_strip(player_name)
        sql = '''
        SELECT  
        COUNT(CASE WHEN fragged = "''' + helpers().safe_string(player_name) + '''" THEN 1 ELSE NULL END) deaths,
        COUNT(CASE WHEN fragger = "''' + helpers().safe_string(player_name) + '''" THEN 1 ELSE NULL END) kills,
        COUNT(CASE WHEN fragger = "SELF" THEN 1 ELSE NULL END) suicides
        from frags
        WHERE
        fragger = "''' + helpers().safe_string(player_name) + '''"
        OR
        fragged = "''' + helpers().safe_string(player_name) + '''"
        '''        
        
        cur.execute(sql)
        row = cur.fetchone()
        stats.deaths = row['deaths']
        stats.kills = row['kills']
        stats.suicides = row['suicides']
        
        return stats
        
    def get_game_stats(self, instance, player_name):

        stats = game_stats()
        conn = db().connect()
        cur = conn.cursor()     
        sql = ''' SELECT * FROM logs where log LIKE "%ClientUserinfoChanged:%" AND log LIKE "%''' + str(player_name) + '''%" ORDER BY added DESC LIMIT 1; '''

        cur.execute(sql)
        result = cur.fetchone()
        if(result == None):
            return None
            
        info_split = result['log'].split("\\")
        stats.player_id = result['log'].split(" ")[2]
        stats.player_name = info_split[1]
        stats.model = info_split[5]
        stats.class_id = int(info_split[19])
        stats.class_name = classes.game_classes[stats.class_id]
        stats.instance = result['instance']
        stats.last_played = result['added']
        
        return stats
    
    def client_info_print(self):
    
        print("-------------------------------------------")
        print(bcolors.GREEN + "Last Game" + bcolors.ENDC)
        print("-------------------------------------------")        
        print(bcolors.CYAN + "Name: " + bcolors.ENDC + "{}".format(self.game_stats.player_name))
        print(bcolors.CYAN + "Instance: " + bcolors.ENDC + "{}".format(self.game_stats.instance))
        print(bcolors.CYAN + "Last Played: " + bcolors.ENDC + "{}".format(self.game_stats.last_played))
        print(bcolors.CYAN + "ID: " + bcolors.ENDC + "{}".format(self.game_stats.player_id))
        print(bcolors.CYAN + "Class: " + bcolors.ENDC + "{}".format(self.game_stats.class_name))
        print("-------------------------------------------")
        print(bcolors.GREEN + "Global Stats" + bcolors.ENDC)
        print("-------------------------------------------")        
        print(bcolors.CYAN + "Kills: " + bcolors.ENDC + "{}".format(self.global_stats.kills))
        print(bcolors.CYAN + "Deaths: " + bcolors.ENDC + "{}".format(self.global_stats.deaths))
        print(bcolors.CYAN + "Suicides: " + bcolors.ENDC + "{}".format(self.global_stats.suicides))        

        