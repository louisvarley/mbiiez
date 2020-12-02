import sqlite3
import datetime

from sqlite3 import Error

from mbiiez import settings
from mbiiez.helpers import helpers

class db:

    def __init__(self):
        """ generates schema if not already created """
        self.generate_schema()

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    """ Create a database connection to a SQLite database """    
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(settings.database.database)
            conn.row_factory = self.dict_factory
            return conn
        except Error as e:
            print(e)

    """ Create a table using SQL """
    def create_table(self, create_table_sql):
     
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    """ Delete from a table using ID Column """   
    def delete(self, table, id):
        sql = ''' DELETE FROM ''' + table + ''' Where id == "''' + str(id) + '''"'''
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    """ create an entry to given table using a data dictionary """            
    def insert(self, table, d):
        f = ''
        v = []
        q = ""
        
        d["added"] = str(datetime.datetime.now())
        
        for key in d.keys():
            f = "{},{}".format(f, key)
            v.append(helpers().ansi_strip(str(d[key])))
            q = "{},{}".format(q,"?")
            
       
        f = f[1:] #""" Keys """
        q = q[1:] #""" Place Holders """  
        v = tuple(v)     #""" Turple of values """   
          
        sql = ''' INSERT INTO ''' + table + '''(''' + f + ''')
                  VALUES(''' + q + ''') '''
                  
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, v)
        conn.commit()
        return cur.lastrowid 
        
    """ Use a dictionary to find matching entries """    
    def select(self, table, d):
    
        w = ''
        v = []
        conn = self.connect()
        cur = conn.cursor()

        for key in d.keys():
            w = w + "{}=? AND ".format(key)
            v.append(helpers().ansi_strip(d[key]))

        v = tuple(v)     #""" Turple of values """   
        w = w[:-4] #""" Keys """    
        q = ''' SELECT * FROM ''' + table + ''' WHERE ''' + w
        cur.execute(q, v)
        rows = cur.fetchall()
        return rows
      
    def temp_get_player_id(self, player):
        conn = self.connect()
        cur = conn.cursor()
        player = helpers().ansi_strip(player)     
        q = ''' SELECT * FROM connections where player == "''' + player + '''" and type = "CONNECT" ORDER BY added DESC LIMIT 1; '''
        cur.execute(q)
        rows = cur.fetchall()
        return rows       
        
        
    def generate_schema(self):
        
        self.create_table("""
        CREATE TABLE IF NOT EXISTS chatter (
            id integer PRIMARY KEY AUTOINCREMENT,
            added datetime,
            player text,
            instance text,
            type text,
            message varchar
        );""")
        
        self.create_table("""
        CREATE TABLE IF NOT EXISTS logs (
            id integer PRIMARY KEY AUTOINCREMENT,
            added datetime,
            log text,
            instance text
        );""")        
        
        self.create_table("""
        CREATE TABLE IF NOT EXISTS frags (
            id integer PRIMARY KEY AUTOINCREMENT,
            added datetime,
            instance text,
            fragger text,
            fragged text,
            weapon text
        );""")
        
        self.create_table("""
        CREATE TABLE IF NOT EXISTS connections (
            id integer PRIMARY KEY AUTOINCREMENT,
            added datetime,            
            player_id integer,
            player text,
            instance text,
            ip text,
            type text
        );""")
              
        self.create_table("""
        CREATE TABLE IF NOT EXISTS processes (
            id integer PRIMARY KEY AUTOINCREMENT,
            added datetime,            
            pid integer,
            name text,
            instance text
        );""")        
        
        