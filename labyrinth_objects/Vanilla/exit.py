from random import choice
from labyrinth_engine import Location


class Exit(Location):
    def __init__(self):
        self.must_be_here = set()
        self.add_flag('safe_zone')

    def set_settings(self, settings, locations, items, creatures, players):
        self.ENTER_MSG = settings['enter_msg']['ru']
        self.STAY_MSGS = settings['stay_msgs']['ru']
        self.WIN_MSG = settings['win_msg']['ru']
        self.LOOSE_MSG = settings['loose_msg']['ru']

    def main(self):
        now_here = self.get_children(['player'])

        winners = {true_tres.get_parent() for true_tres in self.labyrinth.get_unique('treasures')}
        if winners & now_here:
            for player in winners & now_here
            self.labyrinth.send_msg(self.WIN_MSG, winner)
            for player in set(self.labyrinth.get_objects('player')) - set([winner]):
                self.labyrinth.send_msg(self.LOOSE_MSG, player)
            self.labyrinth.end_game()
            return

        for player in now_here - self.must_be_here:
            self.labyrinth.send_msg(self.ENTER_MSG, player, 5)
        for player in now_here & self.must_be_here:
            self.labyrinth.send_msg(choice(self.STAY_MSGS), player, 5)
        self.must_be_here = now_here
