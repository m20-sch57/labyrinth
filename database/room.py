from database.db_answer import DBAnswer, DBError, OK
from database.db_table import DBTable
from database.common_functions import *
import json


class Room:
    def __init__(self, ID, name, creator, description, users, date, map_id, db):
        self.id = ID
        self.name = name
        self.description = description
        self.creator = creator
        self.usernames = usernames_from_string(users)
        self.users = list(map(db.users.get_by_name, self.usernames))
        self.date = date
        self.map_id = map_id

    def __str__(self):
        return 'id: {}; name: {}; date: {}'.format(self.id, self.name, self.date)

def usernames_from_string(users_string):
    return json.loads(users_string)

def usernames_to_string(users):
    return json.dumps(users)


class RoomsTable(DBTable):

    def add(self, ID, creator):
        if not self.db.users.have_user(creator):
            return DBAnswer(False, DBError.IncorrectUser,
                            'Can\'t create a room with creator, which are not user.')

        name = 'Комната ' + ID
        description = 'This room has no description'

        # TODO: check ID or gen it here.

        self.execute('''INSERT INTO rooms (id, name, description, creator, create_date, users) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, '[]')''', [ID, name, description, creator])

        return DBAnswer(True, OK, 'Room successfully created')

    def get(self, ID):
        data = self.execute('SELECT * FROM rooms WHERE id=?', [ID])
        room = data.fetchone()

        if room is None:
            return None
        return Room(*room, self.db)

    def delete(self, ID):
        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist,
                            'Can\'t delete nonexistent room')

        self.execute('DELETE FROM rooms WHERE id=?', [ID])
        return DBAnswer(True, OK, 'Room successfully deleted')

    def set_name(self, ID, name):
        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist,
                            'Can\'t set name for nonexistent room')
        if False:  # TODO check, that name is correct
            return DBAnswer(False, DBError.IncorrectRoomName,
                            'Name contains invalid characters')

        self.execute('UPDATE rooms SET name=? WHERE id=?', [name, ID])
        return DBAnswer(True, OK, 'Room name successfully set')

    def set_description(self, ID, description):
        # TODO Answer
        self.execute('UPDATE rooms SET description=? WHERE id=?', [description, ID])

    def add_user(self, ID, username=None):
        if username is None:
            return self.add_user(ID, self.db.users.current_username())

        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist,
                            'Can\'t add user into nonexistent room')
        if not self.db.users.have_user(username):
            return DBAnswer(False, DBError.IncorrectUser,
                            'Can\'t add nonexistent user into room')

        users = self.get(ID).usernames

        if username in users:
            return DBAnswer(False, DBError.IncorrectUser, 'This user already in this room')

        users.append(username)
        users_string = usernames_to_string(users) 
        self.execute('UPDATE rooms SET users=? WHERE id=?', [users_string, ID])

        return DBAnswer(True, OK, 'User successfully added')

    def remove_user(self, ID, username=None):
        if username is None:
            return self.remove_user(ID, self.db.users.current_username())

        if self.get(ID) is None:
            return DBAnswer(False, DBError.RoomNotExist,
                            'Can\'t remove user from nonexistent room')

        usernames = self.get(ID).usernames

        if username not in usernames:
            return DBAnswer(False, DBError.IncorrectUser, 'This user not in this room')

        usernames.remove(username)
        usernames_string = usernames_to_string(usernames)
        self.execute('UPDATE rooms SET users=? WHERE id=?', [usernames_string, ID])

        return DBAnswer(True, OK, 'User successfully removed')

    def get_all(self):
        data = self.execute('SELECT id FROM rooms')
        return [self.get(ID[0]) for ID in data.fetchall()]

    def page_by_page(self, rooms_on_page):
        return break_list(self.get_all(), rooms_on_page)

    def set_map(self, ID, map_id):
        # TODO Answer
        self.execute('UPDATE rooms SET map_id=? WHERE id=?', [map_id, ID])
        return DBAnswer(True, OK, 'Map successfully set')
