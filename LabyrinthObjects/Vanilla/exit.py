from random import choice
from LabyrinthEngine import Location


class Exit(Location):
    def __init__(self):
        self.must_be_here = set()
        self.add_flag('safe_zone')

    def set_settings(self, settings, locations, items, creatures, players):
        self.ENTER_MSG = settings['enter_msg']['ru']
        self.STAY_MSGS = settings['stay_msgs']['ru']

    def main(self):
        now_here = self.get_children(['player'])
        for player in now_here - self.must_be_here:
            self.labyrinth.send_msg(self.ENTER_MSG, player, 5)
        for player in now_here & self.must_be_here:
            self.labyrinth.send_msg(choice(self.STAY_MSGS), player, 5)
        self.must_be_here = now_here
