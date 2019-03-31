from random import choice
from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Location


class Exit(Location):
    def __init__(self):
        self.must_be_here = set()
        self.add_flag('safe_zone')

    def set_settings(self, settings, locations, items, creatures, players):
        self.EXIT_GREETING_MSG = settings['enter_msg']['ru']
        self.EXIT_PRESENCE_MSGS = settings['stay_msgs']['ru']

    def main(self):
        now_here = self.get_children(['player'])
        for player in now_here - self.must_be_here:
            self.labyrinth.send_msg(self.EXIT_GREETING_MSG, player)
        for player in now_here & self.must_be_here:
            self.labyrinth.send_msg(choice(self.EXIT_PRESENCE_MSGS), player)
        self.must_be_here = now_here
