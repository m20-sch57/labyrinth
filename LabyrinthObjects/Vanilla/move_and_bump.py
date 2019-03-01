from Vanilla.consts import *
from LabyrinthEngine import Location, Item


class Legs(Item):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function=lambda: True, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=lambda: True, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=lambda: True, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=lambda: True, turn_name=LEFT_TURN)

    def set_settings(self, settings, locations, items, npcs, players):
        self.WALL_MSG = settings['consts'].get('wall_msg') or WALL_MSG

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = active_player.get_parent().get_neighbour(direction)
            if type(next_position) in borders:
                self.labyrinth.send_msg(self.WALL_MSG, active_player)
            else:
                active_player.set_parent(next_position)

        return move


class EmptyLocation(Location):
    def set_settings(self, settings, locations, items, npcs, players):
        self.ENTER_MSG = settings['consts'].get('enter_msg') or ENTER_MSG
        self.set_name(settings['name'])

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if next_active_player.get_parent() == self:
            self.labyrinth.send_msg(self.ENTER_MSG, next_active_player)


class Outside(Location):
    pass


# Just prototype. But it's more useful than new Wall sometimes...
class GlobalWall(Location):

    def __init__(self, *args):
        # Every argument must be like: (first_loc_i, second_loc_i, dir_from_first_to_second_i).

        self.behind_the_wall = {}
        for tup in args:
            if type(tup) is not tuple or len(tup) != 3:
                raise TypeError('Every argument of GlobalWall must be tuple with 3 items.')
            if type(tup[2]) is not str:
                raise TypeError('Every direction in arguments of GlobalWall must be string.')
            d0 = self.behind_the_wall.get(tup[0], {})
            if tup[2] in d0:
                raise ValueError('There are two walls in same direction of some room.')
            d0[tup[2]] = tup[1]
            self.behind_the_wall[tup[0]] = d0
            d1 = self.behind_the_wall.get(tup[1], {})
            if reverse_direction(tup[2]) in d1:
                raise ValueError('There are two walls in same direction of some room.')
            d1[reverse_direction[tup[2]]] = tup[0]
            self.behind_the_wall[tup[1]] = d1
        # behind_the_wall is dict of dicts. For location on i-th place will be dict like
        # {'direction1': location_in_direction1_behind_wall, ...}.
        # So all list looks like {loc1: {'dir1': loc_in_dir1, ...}, ...}.

    def break_wall(self, object_1, direction):
        if not isinstance(object_1, Location):
            raise ValueError('First argument of GlobalWall.break_wall must be instance of Location.')
        object_2 = self.behind_the_wall[object_1][direction]
        object_1.set_neighbour(direction, object_2)
        object_2.set_neighbour(reverse_direction[direction], object_1)
        del self.behind_the_wall[object_1][direction]
        del self.behind_the_wall[object_2][reverse_direction[direction]]

    def make_wall(self, object_1, direction):
        if not isinstance(object_1, Location):
            raise ValueError('First argument of GlobalWall.break_wall must be instance of Location.')
        object_2 = object_1.get_neighbour(direction)

        d1 = self.behind_the_wall.get(object_1, {})
        if direction in d1:
            raise ValueError('Invalid arguments for GlobalWall.make_wall. '
                             'There is already wall between first room and some another in the direction.')
        d1[direction] = object_2
        self.behind_the_wall[object_1] = d1
        object_1.set_neighbour(direction, self)

        d2 = self.behind_the_wall.get(object_2, {})
        if reverse_direction[direction] in d2:
            raise ValueError('Invalid arguments for GlobalWall.make_wall. '
                             'There is already wall between first room and some another in the direction.')
        d2[reverse_direction[direction]] = object_1
        self.behind_the_wall[object_2] = d2
        object_2.set_neighbour(reverse_direction[direction], self)


class Wall(Location):
    def __init__(self, *args):
        pass
        # Every argument must be like: (from_loc_i, dir_i, to_loc_i).

        # self.behind_the_wall = {}
        # for i in range(len(args)):
        #     tup = args[i]
        #     if type(tup) is not tuple or len(tup) != 3:
        #         raise TypeError('Every argument of Wall must be tuple with 3 items.')
        #     if type(tup[1]) is not str:
        #         raise TypeError('Every direction in arguments of Wall must be string.')
        #     d = self.behind_the_wall.get(tup[0], {})
        #     if tup[1] in d:
        #         raise ValueError('There are two walls in same direction of some room.')
        #     d[tup[1]] = tup[2]
        #     self.behind_the_wall[tup[0]] = d

        # behind_the_wall is dict of dicts. For location on i-th place will be dict like
        # {'direction1': location_in_direction1_behind_wall, ...}.
        # So all list looks like {loc1: {'dir1': loc_in_dir1, ...}, ...}.

    def set_settings(self, settings, locations, *args):
        self.behind_the_wall = {}

        for block in settings['block']:
            d = self.behind_the_wall.get(block['from'], {})
            d[block['dir']] = locations[block['to']]
            self.behind_the_wall[locations[block['from']]] = d

    def break_wall(self):
        for loc in self.behind_the_wall:
            for direction in self.behind_the_wall[loc]:
                neighbour = self.behind_the_wall[loc][direction]
                loc.set_neighbour(direction, neighbour)

        self.labyrinth.locations.discard(self)


borders = [Outside, Wall, GlobalWall]
