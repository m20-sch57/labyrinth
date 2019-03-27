from database.db_answer import DBAnswer, DBError, OK
from database.common_functions import *
import json


class Room:
    def __init__(self, ID, name, creator, description, users, date):
        self.id = ID
        self.name = name
        self.description = description
        self.creator = creator
        self.users = users
        self.date = date

    def __str__(self):
        return 'id: {}; name: {}; date: {}'.format(self.id, self.name, self.date)

def users_from_string(users_string):
    return json.loads(users_string)

def users_to_string(users):
    return json.dumps(users)


class RoomsTable:
    def __init__(self, db):
        self.db = db
        self.connect, self.cursor = self.db.connect, self.db.cursor

    def add(self, ID, creator):
        if not self.db.users.have_user(creator):
            return DBAnswer(False, DBError.IncorrectUser, 
                   'Can\'t create a room with creator, which are not user.')

        name = 'Room by ' + creator
        description = 'This room has no description'

        # TODO: check ID or gen it here.

        self.cursor.execute('''INSERT INTO rooms (id, name, description, creator, create_date, users) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, '[]')''', [ID, name, description, creator])
        self.connect.commit()

        return DBAnswer(True, OK, 'Room successfully created')

    def get(self, ID):
        self.cursor.execute('SELECT * FROM rooms WHERE id=?', [ID])
        room = self.cursor.fetchone()

        if room is None:
            return None
        return Room(*room)

    def delete(self, ID):
        # TODO Answer

        self.cursor.execute('DELETE FROM rooms WHERE id=?', [ID])
        self.connect.commit()

    def set_name(self, ID, name):
        # TODO Answer
        self.cursor.execute('UPDATE rooms SET name=? WHERE id=?', [name, ID])
        self.connect.commit()

    def set_description(self, ID, description):
        # TODO Answer
        self.cursor.execute('UPDATE rooms SET description=? WHERE id=?', [description, ID])
        self.connect.commit()

    def add_user(self, ID, username = None):
        if username is None:
            return self.add_user(ID, self.db.users.current())

        users_string = self.get(ID).users
        users = users_from_string(users_string)

        # TODO check, that user in db

        if username in users:
            return DBAnswer(False, DBError.IncorrectUser, 'This user already in this room')

        users.append(username)
        users_string = users_to_string(users) 
        self.cursor.execute('UPDATE rooms SET users=? WHERE id=?', [users_string, ID])

        return DBAnswer(True, OK, 'User successfully added')

    def remove_user(self, ID, username = None):
        if username is None:
            return self.add_user(ID, self.db.users.current())

        users_string = self.get(ID).users
        users = users_from_string(users_string) 

        if username not in users:
            return DBAnswer(False, DBError.IncorrectUser, 'This user not in this room')

        users.remove(username)
        users_string = users_to_string(users)
        self.cursor.execute('UPDATE rooms SET users=? WHERE id=?', [users_string, ID])

        return DBAnswer(True, OK, 'User successfully removed')

    def page_by_page(self, rooms_on_page):
        self.cursor.execute('SELECT id FROM rooms')
        # print(self.cursor.fetchall())
        rooms = [self.get(ID[0]) for ID in self.cursor.fetchall()]
        return break_list(rooms, rooms_on_page)

