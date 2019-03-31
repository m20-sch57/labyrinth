from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Location


class EmptyLocation(Location):
    def __init__(self):
        self.used = set()

    def set_settings(self, settings, locations, items, creatures, players):
        self.ENTER_MSG = settings.get('enter_msg') or ENTER_MSG
        self.FIRST_ENTER_MSG = settings.get('first_enter_msg') or self.ENTER_MSG

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()

        if next_active_player.get_parent() == self:
            if next_active_player in self.used:
                self.labyrinth.send_msg(self.ENTER_MSG, next_active_player)
            else:
                self.used.add(next_active_player)
                self.labyrinth.send_msg(self.FIRST_ENTER_MSG, next_active_player)
