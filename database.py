# encoding: utf-8


import sqlite3
import os
import base64
import random
import string


'''
help functions
'''


def break_list(lst, cnt):
    n = len(lst)
    res = []
    for i in range(0, n, cnt):
        res.append(lst[i : min(n, i + cnt)])

    if len(res) == 0:
        res.append([])

    return res

def gen_file_name(path, size):
    name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    while name in list(map(lambda x: ''.join(x.split('.')[::-1]), os.listdir(path))):
        name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    return name


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            login VARCHAR(32) PRIMARY KEY, 
            password_hash VARCHAR(40),
            room_id CHAR(8),
            avatar TEXT,
            FOREIGN KEY (room_id) REFERENCES rooms (room_id)
            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS maps (
            maplink VARCHAR(128) PRIMARY KEY, 
            description TEXT
            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
            room_id CHAR(8) PRIMARY KEY, 
            name VARCHAR(128),
            players_in_game TEXT,
            creator VARCHAR(32),
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
            self.cursor.execute("INSERT INTO users (login, password_hash, room_id, avatar) VALUES (?, ?, NULL, 'default.png')", (login, password_hash))
            self.conn.commit()
            return True

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE login=?', (user_id,))
        return self.cursor.fetchone()

    def get_user_password_hash(self, user_id):
        return self.get_user(user_id)[1]  # password_hash

    def set_user_login(self, user_id, login):
        self.cursor.execute('UPDATE users SET login=? WHERE login=?', (login, user_id))
        self.conn.commit()

    def set_user_password_hash(self, user_id, password_hash):
        self.cursor.execute('UPDATE users SET password_hash=? WHERE login=?', (password_hash, user_id))
        self.conn.commit()

    def set_user_room(self, user_id, room_id):
        self.cursor.execute('UPDATE users SET room_id=? WHERE login=?', (room_id, user_id))
        self.conn.commit()

    def user_login_in_table(self, user_login):
        # return True if login in table and False in other cases
        self.cursor.execute('SELECT * FROM users WHERE login=?', (user_login,))
        return not self.cursor.fetchone() is None

    def change_avatar(self, user_login, avatar_b64):
        startstring = 'data:image/png;base64,'
        path = 'app/static/images/avatars/'

        if not avatar_b64.startswith(startstring):
            return {'ok': 0, 'error': 'incorrect format of avatar string'}
        if not self.get_avatar(user_login) == 'default.png':
            os.remove(path+self.get_avatar(user_login))

        try:
            avatar = base64.decodestring(avatar_b64[len('data:image/png;base64,'):].encode('utf-8'))
        except:
            return {'ok': 0, 'error': 'incorrect format of avatar string'}

        filename = gen_file_name(path, 10)+'.png'

        with open(path+filename, 'wb') as f:
            f.write(avatar)

        self.cursor.execute('UPDATE users SET avatar=? WHERE login=?', (filename, user_login))

        return {'ok': 1}

    def get_avatar(self, user_login):
        return self.get_user(user_login)[3]

    '''
    rooms functions
    '''

    def parse_room(self, room):
        if room is None:
            return None
        self.cursor.execute('SELECT * FROM users WHERE room_id=?', (room[0],))
        players_set = set(map(lambda user: user[0], self.cursor.fetchall()))
        room_dir = {
            'room_id': room[0],
            'name': room[1],
            'creator': room[3],
            'players_in_game': room[2],
            'players_set': players_set,
            'settings': room[4],
            'description': room[5],
            'create_date': room[6]
        }
        return room_dir

    def add_room(self, room_id, creator_id):
        crid = creator_id
        self.cursor.execute('''INSERT INTO rooms (room_id, players_in_game, name, creator, create_date) 
            VALUES (?, NULL, ?, ?, CURRENT_TIMESTAMP)''', (room_id, ('Room by '+crid), crid))
        self.conn.commit()

    def get_room(self, room_id):
        self.cursor.execute('SELECT * FROM rooms WHERE room_id=?', (room_id,))
        room = self.cursor.fetchone()
        return self.parse_room(room)

    def get_all_rooms(self):
        self.cursor.execute('SELECT * FROM rooms')
        rooms = self.cursor.fetchall()
        return list(map(lambda room: self.get_room(room[0]), rooms))

    def get_rooms_page_by_page(self):
        self.cursor.execute('SELECT * FROM rooms')
        rooms = list(map(self.parse_room, self.cursor.fetchall()))
        return break_list(rooms, 6)

    def delete_room(self, room_id):
        self.cursor.execute('DELETE FROM rooms WHERE room_id=?', (room_id,))
        self.conn.commit()

    def delete_all_rooms(self):
        self.cursor.execute('DELETE FROM rooms')
        self.conn.commit()

    def get_room_name(self, room_id):
        return self.get_room(room_id)['name']
    def get_room_creator(self, room_id):
        return self.get_room(room_id)['creator']
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
        self.set_user_room(user_id, room_id)
       
    def remove_player(self, room_id, user_id):
        self.set_user_room(user_id, 'NULL') 

    def start_game(self, room_id):
        self.cursor.execute('UPDATE rooms SET players_in_game=? WHERE room_id=?', (','.join(self.get_room_players(room_id)), room_id))

    def end_game(self, room_id):
        self.cursor.execute('UPDATE rooms SET players_in_game=NULL WHERE room_id=?', (room_id,))

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
