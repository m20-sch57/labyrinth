from random import choice
from labyrinth_engine import Location, Item


class Exit(Location):
    def __init__(self):
        super().__init__()

        self.must_be_here = set()
        self.add_flag('safe_zone')

    def set_settings(self, settings, locations, items, creatures, players):
        self.ENTER_MSG = settings['enter_msg']['ru']
        self.STAY_MSGS = settings['stay_msgs']['ru']

    def main(self):
        now_here = self.get_children('player')

        for player in now_here - self.must_be_here:

            self.labyrinth.send_msg(self.ENTER_MSG, player, 5)
        for player in now_here & self.must_be_here:
            self.labyrinth.send_msg(choice(self.STAY_MSGS), player, 5)
        self.must_be_here = now_here


class ExitChecker(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.WIN_MSG = settings['win_msg']['ru']
        self.LOOSE_MSG = settings['loose_msg']['ru']

    def main(self):
        players_in_exits = set(self.labyrinth.get_objects(['player'], key=(lambda pl: type(pl.get_parent()) is Exit)))
        winners = set(filter(lambda player: bool(player.get_children(flags='true_tres')),
                             players_in_exits))

        if winners:
            for winner in winners:
                self.labyrinth.send_msg(self.WIN_MSG, winner)
            for looser in set(self.labyrinth.get_objects('player')) - winners:
                self.labyrinth.send_msg(self.LOOSE_MSG, looser)
            self.labyrinth.end_game()
