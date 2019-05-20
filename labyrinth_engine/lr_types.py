from labyrinth_engine import LabyrinthObject as LO


class Location(LO):
    _lrtype = 'location'


class Item(LO):
    _lrtype = 'item'


class Player(LO):
    """
    Class of players of the game
    """

    _lrtype = 'player'

    def __init__(self, username):
        self.name = self.username = username

    def get_username(self):
        return self.username

    def skip_turns(self, count):
        self.delete_flag('skip_turns')
        if count:
            self.set_flag('skip_turns', count)


class Creature(LO):
    _lrtype = 'creature'
