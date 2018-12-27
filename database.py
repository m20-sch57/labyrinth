#encoding: utf-8


import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            login text PRIMARY KEY,
            pass_hash text,
            room integer)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS maps (
            id integer PRIMARY KEY, 
            maplink text, 
            description text)''') #description

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
            id integer PRIMARY KEY, 
            joinlink text, 
            settings text, 
            description text, 
            creator text, 
            cr_date text, 
            pl_num integer)''') #settings
        
        self.conn.commit()
        
    def quit(self):
        self.conn.close()
        
    def add_user(self, login, pass_hash):
        user_data = [login, pass_hash]
        self.cursor.execute('INSERT INTO users VALUES (?, ?, -1)', user_data) #-1 - игрок не в комнате, иначе он в комнате с нужным id
        self.conn.commit()
        
    def add_map(self, maplink, description):
        map_data = [maplink, description]
        self.cursor.execute('INSERT INTO maps VALUES (NULL, ?, ?)', map_data)
        self.conn.commit()
    
    def add_room(self, joinlink, settings, description, creator):
        room_data = [joinlink, settings, description, creator]
        self.cursor.execute('INSERT INTO rooms VALUES (NULL, ?, ?, ?, ?, CURRENT_TIMESTAMP, 1)', room_data)
        self.conn.commit()
    
    def get_user(self, login):
        self.cursor.execute('SELECT * FROM users WHERE login=?', [login])
        return self.cursor.fetchone()
    
    def get_map(self, mapid):
        self.cursor.execute('SELECT * FROM maps WHERE id=?', [mapid])
        return self.cursor.fetchone()
    
    def get_room(self, roomid):
        self.cursor.execute('SELECT * FROM rooms WHERE id=?', [roomid])
        return self.cursor.fetchone()

    def get_room_by_link(self, joinlink):
        self.cursor.execute('SELECT * FROM rooms WHERE joinlink=?', [joinlink])
        return self.cursor.fetchone()
    
    def add_player(self, roomid, player):
        data = self.get_user(player)
        self.cursor.execute('DELETE FROM users WHERE login=?', [player])
        data = list(data)
        data[2] = roomid
        self.cursor.execute('INSERT INTO users VALUES(?, ?, ?)', data)
        self.conn.commit()
       
    def remove_player(self, player):
        data = self.get_user(player)
        self.cursor.execute('DELETE FROM users WHERE login=?', [player])
        data = list(data)
        data[2] = -1
        self.cursor.execute('INSERT INTO users VALUES(?, ?, ?)', data)
        self.cursor.execute('DELETE FROM rooms WHERE pl_num = 0')
        self.conn.commit()
        
    def get_pages(self): 
        pages = []
        self.cursor.execute('SELECT * FROM rooms')
        for i in range(3):
            pages.append(self.cursor.fetchmany(size=6))
        return pages
    
    
    def update_db(self):
        self.cursor.execute('DROP TABLE rooms')
        self.cursor.execute('DROP TABLE users')
        self.cursor.execute('DROP TABLE maps')
        self.conn.commit()
        
