import sqlite3

from database.room import RoomsTable
from database.user import UsersTable
from database.map import MapsTable
from database.lr_manager import LRManager


def connection():
    connect = sqlite3.connect('database.db', check_same_thread=False)
    cursor = connect.cursor
    return cursor, connect


def init_db():
    cursor, connect = connection()

    cursor().execute('''CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT, 
                    password_hash TEXT,
                    avatar TEXT
                    )''')

    cursor().execute('''CREATE TABLE IF NOT EXISTS rooms (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    creator TEXT,
                    description TEXT, 
                    users TEXT,
                    create_date TEXT,
                    map_id INTEGER,
                    FOREIGN KEY (creator) REFERENCES users (username)
                    )''')

    cursor().execute('''CREATE TABLE IF NOT EXISTS maps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    creator TEXT,
                    description TEXT,
                    map TEXT)''')


def drop_db():
    cursor, connect = connection()

    init_db()
    cursor().execute('DROP TABLE rooms')
    cursor().execute('DROP TABLE users')
    cursor().execute('DROP TABLE maps')
    connect.commit()


class Database:
    def __init__(self):
        init_db()
        self.cursor, self.connect = connection()
        self.users = UsersTable(self)
        self.rooms = RoomsTable(self)
        self.maps = MapsTable(self)
        self.lrm = LRManager(self)
