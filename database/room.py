from db_answer import DBAnswer, DBError, OK
from common_functions import *


class Room:
    def __init__(self, ID, name, description, creator, users, playing_users, date):
        self.id = ID
        self.name = name
        self.description = description
        self.creator = creator
        self.users = users
        self.date = date

    def __str__(self):
        return 'id: {}; name: {}; date: {}'.format(self.id, self.name, self.date)


class RoomsTable:
    def __init__(self, db):
        self.connect, self.cursor = connection()
        self.db = db

    def add(self, ID, creator):
        if not self.db.users.have_user(creator):
            return DBAnswer(False, DBError.NoSuchUser, 
                   'Can\'t create a room with creator, which are not user.')

        name = 'Room by ' + creator
        description = 'This room has no description'

        # TODO: check ID or gen it here.

        self.cursor.execute('''INSERT INTO rooms (id, name, description, creator, create_date) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)''', [ID, name, description, creator])
        self.connect.commit()

        return OK

    def get(self, ID):
        self.cursor.execute('SELECT * FROM rooms WHERE id=?', [ID])
        room = self.cursor.fetchone()

        if room is None:
            return None
        return Room(*room)

    def delete(self, ID):
        self.cursor.execute('DELETE FROM rooms WHERE id=?', [ID])
        self.connect.commit()

    def set_name(self, ID, name):
        # TODO
        pass

    def set_description(self, ID, descriptio):
        # TODO
        pass

    def add_player(self, ID, username = None):
        # TODO
        pass

    def remove_player(self, ID, username = None):
        # TODO
        pass

