#encoding: utf-8


import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            login VARCHAR(32) PRIMARY KEY, 
            password_hash VARCHAR(40)
            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS maps (
            maplink VARCHAR(128) PRIMARY KEY, 
            description TEXT
            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
            room_id CHAR(8) PRIMARY KEY, 
            name VARCHAR(128),
            creator VARCHAR(32),
            players_set TEXT,
            settings TEXT, 
            description TEXT, 
            create_date DATETIME,
            FOREIGN KEY (creator) REFERENCES users (login)
            )''') 

        self.conn.commit()

   

    '''
    users functions
    '''
        
    def add_user(self, login, password_hash):
        '''
        Return False if user with such login alredy employed

        Adds the user in db and return True if login is free
        '''
        if self.user_login_in_table(login):
            return False
        else:
            self.cursor.execute("INSERT INTO users (login, password_hash) VALUES (?, ?)", (login, password_hash))
            self.conn.commit()
            return True


    def get_user(self, login):
        self.cursor.execute('SELECT * FROM users WHERE login=?', (login,))
        return self.cursor.fetchone()

    def get_user_password_hash(self, login):
        return self.get_user(login)[1] # password_hash


    def set_user_login(self, user_id, login):
        if self.user_login_in_table(login):
            return False
        else:
            self.cursor.execute('UPDATE users SET login=? WHERE login=?', (login, login))
            self.conn.commit()    
            return True

    def set_user_password_hash(self, user_id, password_hash):
        self.cursor.execute('UPDATE users SET password_hash=? WHERE user_id=?', (password_hash, str(user_id)))
        self.conn.commit()


    def user_login_in_table(self, user_login):
        # return True if login in table and False in other cases
        self.cursor.execute('SELECT * FROM users WHERE login=?', (user_login,))
        return not self.cursor.fetchone() == None


    '''
    rooms functions

    ''' 
    def parse_room(self, room):
        room_dir = {
            'room_id': room[0],
            'name': room[1],
            'creator': room[2],
            # convert string into list, then convert into set
            'players_set': set(room[3].split(',')),
            'settings': room[4],
            'description': room[5],
            'create_date': room[6]
        }
        return room_dir

    def add_room(self, room_id, creator_id):
        crid = creator_id
        self.cursor.execute('''INSERT INTO rooms (room_id, name, creator, players_set, create_date) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''', (room_id, ('Room by '+crid), crid, crid))
        self.conn.commit()

    def get_room(self, room_id):
        self.cursor.execute('SELECT * FROM rooms WHERE room_id=?', (room_id,))
        room = self.cursor.fetchone()
        return self.parse_room(room)

    def get_all_rooms(self):
        self.cursor.execute('SELECT * FROM rooms')
        rooms = self.cursor.fetchall()
        return list(map(lambda room: self.get_room(room[0]) ,rooms))

    def get_rooms_page_by_page(self):
        pages = []
        self.cursor.execute('SELECT * FROM rooms')
        for i in range(3):
            # взяли 6 комнат, распарсили, и добавили в pages как list
            pages.append(list(map(lambda room_arr: self.parse_room(room_arr), self.cursor.fetchmany(size=6))))
        return pages

    def delete_room(self, room_id):
        self.cursor.execute('DELETE FROM rooms WHERE room_id=?', (room_id,))
        self.conn.commit()


    def get_room_name(self, room_id):
        return self.get_room(room_id)['name']
    def get_room_creator_id(self, room_id):
        return self.get_room(room_id)['creator_id']
    def get_room_creator_login(self, room_id):
        return self.get_user_login(self.get_creator_id(room_id))
    def get_room_players(self, room_id):
        return self.get_room(room_id)['players_set']
    def get_room_settings(self, room_id):
        return self.get_room()['settings']
    def get_room_description(self, room_id):
        return self.get_room(room_id)['description']
    def get_room_create_date(self, room_id):
        return self.get_room(room_id)['create_date']


    def set_room_name(self, room_id, name):
        self.cursor.execute('UPDATE rooms SET name=? WHERE room_id=?', (name, room_id))
        self.conn.commit()
    def set_settings(self, room_id, settings):
        self.cursor.execute('UPDATE rooms SET settings=? WHERE room_id=?', (settings, room_id))
        self.conn.commit()
    def set_description(self, room_id, description):
        self.cursor.execute('UPDATE rooms SET description=? WHERE room_id=?', (description, room_id))
        self.conn.commit()              


    def add_player(self, room_id, user_id):
        players_set = self.get_room_players(room_id) # set of user_id
        players_set.add(str(user_id)) # add new user_id to list
        self.cursor.execute('UPDATE rooms SET players_set=? WHERE room_id=?', 
            (','.join(list(players_set)), room_id)) # convert into TEXT format

        self.conn.commit()
       
    def remove_player(self, room_id, user_id):
        players_set = self.get_room_players(room_id) # set of user_id
        players_set.discard(str(user_id)) # discart player with respective user_id
        self.cursor.execute('UPDATE rooms SET players_set=?  WHERE room_id=?', 
            (','.join(list(players_set)), room_id)) # convert into TEXT format

        self.conn.commit()     



    '''
    maps functions
    '''
    def add_map(self, maplink, description):
        self.cursor.execute('INSERT INTO maps VALUES (?, ?)', (maplink, description))
        self.conn.commit()


    def get_map(self, maplink):
        self.cursor.execute('SELECT * FROM maps WHERE maplink=?', [maplink])
        return self.cursor.fetchone()



    '''
    another functions
    '''
    def drop(self):
        self.cursor.execute('DROP TABLE rooms')
        self.cursor.execute('DROP TABLE users')
        self.cursor.execute('DROP TABLE maps')
        self.conn.commit()

    def quit(self):
        self.conn.close()       
