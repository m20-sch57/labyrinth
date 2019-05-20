from database.db_answer import DBAnswer, DBError, OK
from database.common_functions import *


class LRManager:
    def __init__(self, db):
        self.list = {}
        self.db = db

    def get_labyrinth(self, room_id):
        return self.list.get(room_id)

    def add_labyrinth(self, room_id, labyrinth):
        if room_id in self.list:
            return DBAnswer(False, DBAnswer.LabyrinthAlreadyExist,
                            'Labyrinth with this room id alredy exists.')
        else:
            self.list[room_id] = labyrinth
            return DBAnswer(True, OK, 'Labyrinth ssuccessfully added.')

    def remove_labyrinth(self, room_id):
        if room_id not in self.list:
            return DBAnswer(False, DBAnswer.LabyrinthNotExist,
                            'Labyrinth with this room id do not exist.')
        else:
            self.list.pop(room_id)
            return DBAnswer(True, OK, 'Labyrinth ssuccessfully removed.')
