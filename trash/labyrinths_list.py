class LabyrinthsList:
    """
    Позволит хранить список игр в оперативной памяти

    room_id - это id комнаты в которой происходит игра
    """

    def __init__(self):
        self.list = {}

    def get_labyrinth(self, room_id):
        if room_id in self.list:
            return self.list[room_id]
        else:
            return None

    def add_labyrinth(self, room_id, labyrinth):
        if room_id in self.list:
            return False
        else:
            self.list[room_id] = labyrinth
            return True

    def remove_labyrinth(self, room_id):
        if room_id in self.list:
            return False
        else:
            self.list.pop(room_id)
            return True
