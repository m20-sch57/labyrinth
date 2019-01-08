from Labyrinth.LS_CONSTS import *
from Labyrinth.game_LR2 import LabyrinthObject as LO, ObjectID as OID


# Item.
class Legs(LO):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function=self.condition, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=self.condition, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=self.condition, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=self.condition, turn_name=LEFT_TURN)

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = self.field.get_neighbour_location(active_player.get_parent_id(), direction)
            if type(next_position) in [GlobalWall, Wall, Outside]:
                self.labyrinth.send_msg(WALL_MSG, active_player.get_user_id())
            else:
                active_player.set_parent_id(next_position.get_object_id())
        return move

    def move(self, character, direction):
        next_position = self.field.get_neighbour_location(character.get_parent_id(), direction)
        if type(next_position) not in [GlobalWall, Wall, Outside]:
            character.set_parent_id(next_position.get_object_id())

    def condition(self):
        return True


# Location.
class EmptyLocation(LO):
    used = {}

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()

        if next_active_player.get_parent_id() == self.object_id:
            if next_active_player.get_object_id().number in self.used:
                self.used[next_active_player.get_object_id().number] += 1
                self.labyrinth.send_msg(ENTER_MSG, next_active_player.user_id)
            else:
                self.used[next_active_player.get_object_id().number] = 1
                self.labyrinth.send_msg(FIRST_ENTER_MSG, next_active_player.user_id)


# Location.
class Outside(LO):
    pass


# Location.
# Just prototype. But it's more useful than new Wall sometimes...
class GlobalWall(LO):
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
                d1[self.reverse_direction[arr[2]]] = arr[0]
                new_arg[arr[1]] = d1
            arg = new_arg
        # behind_the_wall is dict of dicts. For location with ID i on i-th place will be dict like
        # {'direction1': location_in_direction1_behind_wall, ...}.
        # So all list looks like {loc1: {'dir1': loc_in_dir1, ...}, ...}.
        # loc and loc_in_dir are integers (not location or ID) too.
        self.behind_the_wall = arg

    def break_wall(self, object_id_1, direction):
        if type(object_id_1) is not OID:
            raise ValueError('Invalid literal for break_wall()')
        object_id_2 = self.field.locations_list[self.behind_the_wall[object_id_1.number][direction]].get_object_id()
        self.field.adjacence_list[object_id_1.number][direction] = object_id_2.number
        self.field.adjacence_list[object_id_2.number][self.reverse_direction[direction]] = object_id_1.number
        del self.behind_the_wall[object_id_1.number][direction]
        del self.behind_the_wall[object_id_2.number][self.reverse_direction[direction]]

    def make_wall(self, object_id_1, direction):
        if type(object_id_1) is not OID:
            raise ValueError('Invalid literal for make_wall()')
        object_id_2 = self.field.get_neighbour_location_id(object_id_1, direction)
        num_1 = object_id_1.number
        num_2 = object_id_2.number
        self_num = self.get_object_id().number

        d1 = self.behind_the_wall.get(num_1, {})
        if direction in d1:
            raise ValueError('There is already wall between first room and some another in the direction')
        d1[direction] = num_2
        self.behind_the_wall[num_1] = d1
        self.field.adjacence_list[num_1][direction] = self_num

        d2 = self.behind_the_wall.get(num_2, {})
        if self.reverse_direction[direction] in d2:
            raise ValueError('There is already wall between second room and some another in the opposite direction')
        d2[self.reverse_direction[direction]] = num_1
        self.behind_the_wall[num_2] = d2
        self.field.adjacence_list[num_2][direction] = self_num


# Location.
class Wall(LO):
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
            if type(pair) is not tuple or len(pair) != 2 or type(pair[0]) is not int:
                raise ValueError('Invalid literal for Wall')
            d = self.behind_the_wall.get(pair[0], {})
            d[pair[1]] = next_pair[0]
            self.behind_the_wall[pair[0]] = d
        # behind_the_wall is dict of dicts. For location with ID i on i-th place will be dict like
        # {'direction1': location_in_direction1_behind_wall, ...}.
        # So all list looks like {loc1: {'dir1': loc_in_dir1, ...}, ...}.
        # loc and loc_in_dir are integers (not location or ID) too.

    def break_wall(self):
        for num in self.behind_the_wall:
            for direction in self.behind_the_wall[num]:
                neighbour_num = self.behind_the_wall[num][direction]
                self.field.adjacence_list[num][direction] = neighbour_num

        ind = self.get_object_id().number
        del self.field.locations_list[ind]
        for i in range(ind, len(self.field.locations_list)):
            self.field.locations_list[i].get_object_id().number = i
        del self.field.adjacence_list[ind]
        del self
