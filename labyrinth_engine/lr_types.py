from labyrinth_engine import LabyrinthObject as LO


class Location(LO):
    _lrtype = 'location'

    def __init__(self):
        super().__init__()

        self.directions = {}

    def get_neighbour(self, direction):
        if direction not in self.directions:
            raise ValueError(
                'Invalid "direction" argument for LabyrinthObject.get_neighbour: ' + str(direction))
        else:
            return self.directions[direction]

    def set_neighbour(self, direction, neighbour):
        if not isinstance(neighbour, LO) or neighbour.lrtype != 'location':
            raise ValueError(
                'Invalid "neighbour" argument for LabyrinthObject.set_neighbour: ' + str(neighbour))
        else:
            self.directions[direction] = neighbour


class Item(LO):
    _lrtype = 'item'


class Player(LO):
    """
    Class of players of the game
    """

    _lrtype = 'player'

    def __init__(self, username):
        super().__init__()

        self.name = self.username = username

    def get_username(self):
        return self.username


class Creature(LO):
    _lrtype = 'creature'
