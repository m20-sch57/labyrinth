from database.db_answer import DBAnswer, DBError, OK
from database.common_functions import *
import json


class Room:
    def __init__(self, ID, name, creator, description, users, date, map_id):
        self.id = ID
        self.name = name
        self.description = description
        self.creator = creator
        self.users = users_from_string(users)
        self.date = date
        self.map_id = map_id


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
        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist, 
                'Can\'t delete nonexistent room')

        self.cursor.execute('DELETE FROM rooms WHERE id=?', [ID])
        self.connect.commit()
        return DBAnswer(True, OK, 'Room successfully deleted')

    def set_name(self, ID, name):
        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist, 
                'Can\'t set name for nonexistent room')
        if False: # TODO check, that name is correct
            return DBAnswer(False, DBError.IncorrectRoomName, 
                'Name contains invalid characters')

        self.cursor.execute('UPDATE rooms SET name=? WHERE id=?', [name, ID])
        self.connect.commit()
        return DBAnswer(True, OK, '')

    def set_description(self, ID, description):
        # TODO Answer
        self.cursor.execute('UPDATE rooms SET description=? WHERE id=?', [description, ID])
        self.connect.commit()

    def add_user(self, ID, username = None):
        if username is None:
            return self.add_user(ID, self.db.users.current_username())

        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist,
                'Can\'t add user into nonexistent room')
        if not self.db.users.have_user(username):
            return DBAnswer(False, DBError.IncorrectUser, 
                'Can\'t add nonexistent user into room')

        users = self.get(ID).users

        if username in users:
            return DBAnswer(False, DBError.IncorrectUser, 'This user already in this room')

        users.append(username)
        users_string = users_to_string(users) 
        self.cursor.execute('UPDATE rooms SET users=? WHERE id=?', [users_string, ID])
        self.connect.commit()

        return DBAnswer(True, OK, 'User successfully added')

    def remove_user(self, ID, username = None):
        if username is None:
            return self.remove_user(ID, self.db.users.current_username())

        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist,
                'Can\'t remove user from nonexistent room')  

        users = self.get(ID).users

        if username not in users:
            return DBAnswer(False, DBError.IncorrectUser, 'This user not in this room')

        users.remove(username)
        users_string = users_to_string(users)
        self.cursor.execute('UPDATE rooms SET users=? WHERE id=?', [users_string, ID])
        self.connect.commit()

        return DBAnswer(True, OK, 'User successfully removed')

    def page_by_page(self, rooms_on_page):
        self.cursor.execute('SELECT id FROM rooms')
        rooms = [self.get(ID[0]) for ID in self.cursor.fetchall()]
        return break_list(rooms, rooms_on_page)

    def set_map(self, ID, map_id):
        # TODO Answer
        self.cursor.execute('UPDATE rooms SET map_id=? WHERE id=?', [map_id, ID])
        self.connect.commit()
