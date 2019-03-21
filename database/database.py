from flask import session
import sqlite3
from common_functions import *
from enum import IntEnum
import json


class Database:
    def __init__(self):
        self.users = UsersTable()
        self.rooms = RoomsTable()


class DBAnswer:
    def __init__(self, ok, error, info):
        self.ok = ok
        self.error = error
        self.info = info


class DBError(IntEnum):
    AlwaysOk = 0
    IncorrectUsername = 1
    IncorrectPassword = 2
    IncorrectAvatar = 3

OK = DBError.AlwaysOk


class User:
    def __init__(self, ID, username, password_hash, avatar):
        self.id = ID
        self.username = username
        self.password_hash = password_hash
        self.avatar = avatar

    def __str__(self):
        return 'id: {}; username: {}; password_hash: {};'.format(
               self.id, self.username, self.password_hash)

class UsersTable:
    def __init__(self):
        self.connect = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT, 
            password_hash TEXT,
            avatar TEXT
            )''')

    def get_by_name(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username=?', [username])
        user_data = self.cursor.fetchone()
        if user_data is None:
            return None
        return User(*self.cursor.fetchone())

    def get_by_id(self, ID):
        self.cursor.execute('SELECT * FROM users WHERE id=?', [ID])
        user_data = self.cursor.fetchone()
        if user_data is None:
            return None
        return User(*self.cursor.fetchone())

    def current_username(self):
        return session.get('username')

    def current(self):
        return self.get_by_name(self.current_username())

    def user_in_table(self, username):
        return not self.get_by_name(username) is None

    def number_of_users(self):
        self.cursor.execute('SELECT * FROM users')
        return len(self.cursor.fetchall())

    def add(self, username, password):
        if self.user_in_table(username):
            return DBAnswer(False, DBError.IncorrectUsername, 
                'User with same username already exist')
        if False: # TODO check username for length and invalid characters
            return DBAnswer(False, DBError.IncorrectUsername,
                'Username contains invalid characters or too short/long')
        if False: # TODO check password for length and invalid characters
            return DBAnswer(False, DBError.IncorrectPassword,
                'Password contains invalid characters or too short')

        password_hash = sha1_hash(password)
        ID = self.number_of_users()
        avatar = 'default.png'

        self.cursor.execute('''INSERT INTO users (id, username, password_hash, avatar)
                               VALUES (?, ?, ?, ?) ''', [ID, username, password_hash, avatar])
        self.connect.commit()
        return DBAnswer(True, OK, 'User successfully created')


    # password

    def set_password(self, password, username = None):
        if username is None:
            return self.set_password(password, username = self.current_username())
            
        if False: # TODO check password for length and invalid characters
            return DBAnswer(False, DBError.IncorrectPassword,
                'Password contains invalid characters or too short')

        password_hash = sha1_hash(password)
        self.cursor.execute('''UPDATE users SET password_hash=? WHERE username=?''', 
                               [password_hash, username])
        return DBAnswer(True, OK, 'Password successfully changed')


    def check_password(self, password, username = None):
        if username is None:
            return self.check_password(password, self.current_username())

        return self.get_by_name(username).password_hash == sha1_hash(password)

    # username

    def set_username(self, new_username, username = None):
        if username is None:
            return self.set_username(new_username, self.current_username())

        if self.user_in_table(new_username):
            return DBAnswer(False, DBError.IncorrectUsername, 
                'User with same username already exist')
        if False: # TODO check username for length and invalid characters
            return DBAnswer(False, DBError.IncorrectUsername,
                'Username contains invalid characters or too short/long')

        self.cursor.execute('''UPDATE users SET username=? WHERE username=?''', 
                               [new_username, username])
        return DBAnswer(True, OK, 'Username successfully changed')

    # avatar

    def set_avatar(self, avatar, username = None):
        if username is None:
            return self.set_avatar(avatar, self.current_username())

        startstring = 'data:image/png;base64,'
        path = 'app/static/images/avatars/'

        if not avatar_b64.startswith(startstring):
            return DBAnswer(False, DBError.IncorrectAvatar, 
                    'Avatar string must be started with "' + startstring + '"')
        try:
            avatar = base64.decodebytes(avatar_b64[len(startstring):].encode('utf-8'))
        except:
            return DBAnswer(False, DBError.IncorrectAvatar, 
                 'Can\'t decode avatar. It must be encoded with base64 format')

        filename = gen_file_name(path, 10) + '.png'
        if not self.get_by_name(username).avatar == 'default.png':
            os.remove(path + self.get_by_name(username).avatar)
        with open(path + filename, 'wb') as f:
            f.write(avatar)

        self.cursor.execute('UPDATE users SET avatar=? WHERE username=?', 
                                                          (filename, username))

        return DBAnswer(True, OK, 'Avatar successfully changed')


class Room:
    def __init__(self, ID, name, description, creator, users, playing_users, date):
        self.id = ID
        self.name = name
        self.description = description
        self.creator = creator
        self.users = users
        self.users_in_game = users_in_game
        self.playing_users = playing_users
        self.date = date

    def print(self):
        print('id:', self.id)
        print('name', self.name)
        print('date', self.date)


class RoomsTable:
    def __init__(self):
        self.connect = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT, 
            users TEXT,
            playing_users TEXT,
            creator TEXT,
            create_date TEXT,
            FOREIGN KEY (creator) REFERENCES users (username)
            )''')

    def add(self, ID, creator):
        name = 'Room by ' + creator
        description = 'This room has no description'
        self.cursor.execute('''INSERT INTO rooms (id, name, description, creator, create_date) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''', [ID, name, description, creator])
        self.connect.commit()
