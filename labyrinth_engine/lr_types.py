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
        if not isinstance(neighbour, Location):
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

    def set_turns_skip(self, count):
        self.delete_flag('skip_turns')
        if count:
            self.set_flag('skip_turns', count)

    def add_turns_skip(self, count):
        prev_turns_skip = self.get_flag('skip_turns', 0)
        if prev_turns_skip != -1:
            if count + prev_turns_skip > 0:
                self.set_flag('skip_turns', count + prev_turns_skip)
            else:
                self.delete_flag('skip_turns')

    def die(self):
        self.set_turns_skip(-1)

    def revive(self):
        self.delete_flag('skip_turns')


class Creature(LO):
    _lrtype = 'creature'
