from LabyrinthModule.CONSTS import *
from LabyrinthModule.LabyrinthEngine.LTypes import Location, Item


# Item.
class Legs(Item):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function=self.condition, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=self.condition, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=self.condition, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=self.condition, turn_name=LEFT_TURN)

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = active_player.get_parent().get_neighbour(direction)
            if type(next_position) is Wall:
                self.labyrinth.send_msg(WALL_MSG, active_player)
            else:
                active_player.set_parent(next_position)

        return move

    def condition(self):
        return True


# Location.
class EmptyLocation(Location):
    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if next_active_player.get_parent() == self:
            self.labyrinth.send_msg(ENTER_MSG, next_active_player)


# Location.
class Outside(Location):
    pass


# Location.
# Just prototype. But it's more useful than new Wall sometimes...
class GlobalWall(Location):
    reverse_direction = {'up': 'down',
                         'down': 'up',
                         'left': 'right',
                         'right': 'left'}

    def __init__(self, arg):
        if type(arg) is list:
            new_arg = {}
            for arr in arg:
                d0 = new_arg.get(arr[0], {})
                d0[arr[2]] = arr[1]
                new_arg[arr[0]] = d0
                d1 = new_arg.get(arr[1], {})
                d1[reverse_direction[arr[2]]] = arr[0]
                new_arg[arr[1]] = d1
            arg = new_arg
        # behind_the_wall is dict of dicts. For location with ID i on i-th place will be dict like
        # {'direction1': location_in_direction1_behind_wall, ...}.
        # So all list looks like {loc1: {'dir1': loc_in_dir1, ...}, ...}.
        # loc and loc_in_dir are integers (not location or ID) too.
        self.behind_the_wall = arg

    def break_wall(self, object_1, direction):
        if issubclass(Location, object_1):
            raise ValueError('Invalid literal for break_wall()')
        object_2 = self.behind_the_wall[object_1][direction]
        object_1.set_neighbour(direction, object_2)
        object_2.set_neighbour(reverse_direction[direction], object_1)
        del self.behind_the_wall[object_1][direction]
        del self.behind_the_wall[object_2][reverse_direction[direction]]

    def make_wall(self, object_1, direction):
        if issubclass(Location, object_1):
            raise ValueError('Invalid literal for make_wall()')
        object_2 = object_1.get_neighbour(direction)

        d1 = self.behind_the_wall.get(object_1, {})
        if direction in d1:
            raise ValueError('There is already wall between first room and some another in the direction')
        d1[direction] = object_2
        self.behind_the_wall[object_1] = d1
        object_1.set_nrighbour(direction, self)

        d2 = self.behind_the_wall.get(object_2, {})
        if self.reverse_direction[direction] in d2:
            raise ValueError('There is already wall between second room and some another in the opposite direction')
        d2[self.reverse_direction[direction]] = object_1
        self.behind_the_wall[object_2] = d2
        object_2.set_neighbour(reverse_direction[direction], self)


# Location.
class Wall(Location):
    def __init__(self, *args):
        if len(args) == 0:
            raise ValueError('Invalid literal for Wall')
        if type(args[0]) is list:
            if len(args) > 1:
                raise ValueError('Invalid literal for Wall')
            args = args[0]

        self.behind_the_wall = {}
        for i in range(len(args)):
            pair = args[i]
            next_pair = args[(i + 1) % len(args)]
            if type(pair) is not tuple or len(pair) != 2:
                raise ValueError('Invalid literal for Wall')
            d = self.behind_the_wall.get(pair[0], {})
            d[pair[1]] = next_pair[0]
            self.behind_the_wall[pair[0]] = d
        # behind_the_wall is dict of dicts. For location with ID i on i-th place will be dict like
        # {'direction1': location_in_direction1_behind_wall, ...}.
        # So all list looks like {loc1: {'dir1': loc_in_dir1, ...}, ...}.
        # loc and loc_in_dir are integers (not location or ID) too.

    def break_wall(self):
        for loc in self.behind_the_wall:
            for direction in self.behind_the_wall[loc]:
                neighbour = self.behind_the_wall[loc][direction]
                loc.set_neighbour(direction, neighbour)

        self.labyrinth.locations.discard(self)
