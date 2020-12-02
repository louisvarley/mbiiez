import datetime

from mbiiez.db import db
from mbiiez.helpers import helpers

class chatter:

    def new(self, player, instance, type, message):

        d = {"added": str(datetime.datetime.now()), "player":player, "instance": instance, "type": type, "message": message}
        return db().insert("chatter", d)
        
        


class process:

    id = None
    instance = None
    name = None
    pid = None
    added = None
    
    def __init__(self, d):
    
        self.id = d['id']
        self.instance = d['instance']
        self.name = d['name']
        self.pid = d['pid']
        self.added = d['added']

class log:

    def new(self, log, instance):

        d = {"added": str(datetime.datetime.now()), "log": log, "instance": instance}
        return db().insert("logs", d)

class frag:

    def new(self, instance, fragger, fragged, weapon):
    
        d = {"added": str(datetime.datetime.now()), "instance": instance, "fragger": fragger, "fragged": fragged, "weapon": weapon}
        return db().insert("frags", d)
        
    def get_kd(self, player):
    
        kills = 0
        deaths = 0
        suicides = 0
        
        player = helpers().ansi_strip(player)
        sql = '''
        SELECT  
        COUNT(CASE WHEN fragged = "''' + helpers().safe_string(player) + '''" THEN 1 ELSE NULL END) Deaths,
        COUNT(CASE WHEN fragger = "''' + helpers().safe_string(player) + '''" THEN 1 ELSE NULL END) Kills,
        COUNT(CASE WHEN fragger = "SELF" THEN 1 ELSE NULL END) Suicides
        from frags
        WHERE
        fragger = "''' + helpers().safe_string(player) + '''"
        OR
        fragged = "''' + helpers().safe_string(player) + '''"
        '''        
        
        rows = db().select(sql)
        
        for row in rows:
            deaths = row[0]
            kills = row[1]
            suicides = row[2]

        return {"kills": kills, "deaths": deaths, "suicides": suicides}
        
    def get_rank(self, player):
    
        player = helpers().ansi_strip(player)

        sql = '''
            SELECT
            ROW_NUMBER() OVER(ORDER BY points / connections desc) as rank,
            points / connections as points,
            player

            from (

            select 
                SUM(points.COUNT) as points, 
                points.player,
                COUNT(connections.player) as connections

            FROM

            (
            select 
            COUNT(*) as count, 
            fragger as player
            from frags
            WHERE
            fragger <> "SELF"

            group by fragger

            UNION ALL

            select 
            0 - COUNT(*) as count, 
            fragged as player 
            from frags
            WHERE fragged <> "Null"
            and fragger <> "SELF"
            group by fragged
              
            ) points

            JOIN connections connections
            on connections.player = points.player

            GROUP BY points.player
              
              )

            where player = "''' + player + '''"

            order by points desc
        '''

class connection:

    def new(self, player, player_id, instance, ip, type):
    
        d = {"added": str(datetime.datetime.now()), "player": player, "player_id": player_id, "instance": instance, "ip": ip, "type": type}
        return db().insert("connections", d)
        
    def get_player_id_from_name(self, player):
 
        results = db().temp_get_player_id(player);
        
        if(len(results) > 0):
            return results[0]['player_id']
    
        return None