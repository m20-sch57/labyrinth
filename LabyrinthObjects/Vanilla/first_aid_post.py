from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Location


class FirstAidPost(Location):
    def __init__(self):
        self.stayed = set()

    def set_settings(self, settings, *args):
        self.FAP_ENTER_MSG = settings['enter_msg']['ru']
        self.FAP_STAY_MSG = settings['stay_msg']['ru']

    def main(self):
        health = self.labyrinth.get_unique('health')
        new_stayed = set()
        for player in self.get_children(lrtype='player'):
            health.heal(player)
            if player in self.stayed:
                self.labyrinth.send_msg(self.FAP_STAY_MSG, player)
            else:
                self.labyrinth.send_msg(self.FAP_ENTER_MSG, player)
            new_stayed.add(player)
        self.stayed = new_stayed
