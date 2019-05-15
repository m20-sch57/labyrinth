from database.db_answer import DBAnswer, DBError, OK
from database.db_table import DBTable
from database.common_functions import *
import json

class Map:
    def __init__(self, ID, name, creator, description, _map):
        self.id = ID
        self.name = name
        self.creator = creator
        self.description = description
        self.map = _map # map is json string

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'creator': self.creator, 'description': self.description}

    def __str__(self):
        return 'id: {}, name: {}, creator: {}'.format(self.id, self.name, self.creator)


# TODO add checks
class MapsTable(DBTable):

    def add(self, name, creator, description, _map):
        self.execute('''INSERT INTO maps (name, creator, description, map)
                               VALUES (?, ?, ?, ?)''', [name, creator, description, _map])
        return DBAnswer(True, OK, 'Map successfully added')

    def get(self, ID):
        data = self.execute('''SELECT * FROM maps WHERE id=?''', [ID])
        map_data = data.fetchone()
        if map_data is None:
            return None
        return Map(*map_data)

    def get_all(self):
        data = self.execute('''SELECT * FROM maps''')
        return list(map(lambda x: Map(*x), data.fetchall()))

    def change_map(self, ID, new_map):
        self.execute('''UPDATE maps SET map=? WHERE id=?''', [new_map, ID])

    def change_name(self, ID, name):
        self.execute('''UPDATE maps SET name=? WHERE id=?''', [name, ID])

    def change_description(self, ID, description):
        self.execute('''UPDATE maps SET description=? WHERE id=?''', [description, ID])
