from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Location


class EmptyLocation(Location):
    def set_settings(self, settings, locations, items, creatures, players):
        self.ENTER_MSG = settings['consts'].get('enter_msg') or ENTER_MSG
        self.set_name(settings['name'])

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if next_active_player.get_parent() == self:
            self.labyrinth.send_msg(self.ENTER_MSG, next_active_player)