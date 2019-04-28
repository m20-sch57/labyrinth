from database.db_answer import DBAnswer, DBError, OK
from database.common_functions import *
import json

class Map:
    def __init__(self, ID, name, creator, description, map_json):
        self.id = ID
        self.name = name
        self.creator = creator
        self.description = description
        self.map = map_json

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'creator': self.creator, 'description': self.description}

    def __str__(self):
        return 'id: {}, name: {}, creator: {}'.format(self.id, self.name, self.creator)


# TODO add checks
class MapsTable:
    def __init__(self, db):
        self.db = db
        self.connect, self.cursor = self.db.connect, self.db.cursor

    def add(self, name, creator, description, map_json):
        self.cursor.execute('''INSERT INTO maps (name, creator, description, map)
                               VALUES (?, ?, ?, ?)''', [name, creator, description, map_json])
        self.connect.commit()
        return DBAnswer(True, OK, 'Map successfully added')

    def get(self, ID):
        self.cursor.execute('''SELECT * FROM maps WHERE id=?''', [ID])
        map_data = self.cursor.fetchone()
        if map_data is None:
            return None
        return Map(*map_data)

    def get_all(self):
        self.cursor.execute('''SELECT * FROM maps''')
        return list(map(lambda x: Map(*x), self.cursor.fetchall()))

    def change_map(self, ID, new_map):
        self.cursor.execute('''UPDATE maps SET map=? WHERE id=?''', [new_map, ID])
        self.connect.commit()

    def change_name(self, ID, name):
        self.cursor.execute('''UPDATE maps SET name=? WHERE id=?''', [name, ID])
        self.connect.commit()

    def change_description(self, ID, description):
        self.cursor.execute('''UPDATE maps SET description=? WHERE id=?''', [description, ID])
        self.connect.commit()
