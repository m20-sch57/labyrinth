from random import choice
from Vanilla.consts import *
from LabyrinthEngine import Location


# Location.
class Exit(Location):
    def __init__(self):
        self.must_be_here = set()

    def set_settings(self, settings, locations, items, npcs, players):
        self.EXIT_GREETING_MSG = settings['consts'].get('exit_greeting_msg') or EXIT_GREETING_MSG
        self.EXIT_PRESENCE_MSGS = settings['consts'].get('exit_presence_msgs') or EXIT_PRESENCE_MSGS

    def main(self):
        now_here = self.get_children(['player'])
        for player in now_here - self.must_be_here:
            self.labyrinth.send_msg(self.EXIT_GREETING_MSG, player)
        for player in now_here & self.must_be_here:
            self.labyrinth.send_msg(choice(self.EXIT_PRESENCE_MSGS), player)
        self.must_be_here = now_here