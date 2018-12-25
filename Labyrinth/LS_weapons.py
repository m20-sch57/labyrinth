from Labyrinth.LS_CONSTS import *
from Labyrinth.game import LabyrinthObject as LO, ObjectID
from Labyrinth.LS_locations import Wall, Outside


class Legs(LO):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function = self.condition, turn_name = UP_TURN)
        self.new_at(self.turn_move('down'), condition_function = self.condition, turn_name = DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function = self.condition, turn_name = RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function = self.condition, turn_name = LEFT_TURN)

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = self.field.get_neighbour_location(active_player.get_parent_id(), direction)
            if type(next_position) in [Wall, Outside]:
                self.labyrinth.send_msg(WALL_MSG, active_player.get_user_id())
            else:
                active_player.set_parent_id(next_position.get_object_id())
        return move

    def condition(self):
        return True


class Gun(LO):
    def __init__(self):
        self.new_at(self.turn_fire('up'), self.condition, FIRE_UP)
        self.new_at(self.turn_fire('down'), self.condition, FIRE_DOWN)
        self.new_at(self.turn_fire('left'), self.condition, FIRE_LEFT)
        self.new_at(self.turn_fire('right'), self.condition, FIRE_RIGHT)

    def turn_fire(self, direction):
        def fire():
            active_player = self.labyrinth.get_active_player()
            self.counts_of_bul[active_player.get_object_id().number] -= 1

            kicked_players = set()
            met_locations = set()
            current_location = active_player.get_parent_id()
            # TODO: Add HURT_EVBD_IN_SAME_LOC
            while current_location.number not in met_locations:
                current_location = self.field.get_neighbour_location(current_location, direction)
                met_locations.add(current_location.number)
                kicked_players &= set(self.field.get_players_in_location(current_location))
            if not CAN_PLAYER_HURT_HIMSELF:
                kicked_players.discard(active_player.user_id)
            for player in kicked_players:
                if not player.states['hurt']:
                    player.states['hurt'] = True
                else:
                    ind = player.get_object_id().number
                    player.set_object_id(ObjectID('dead_player', len(self.field.dead_players_list)))
                    self.field.dead_players_list.append(player)
                    del self.field.players_list[ind]
                    for i in range(ind, len(self.field.players_list)):
                        self.field.players_list[i].get_object_id().number = i
                    del player.parent_id
                    self.labyrinth.number_of_players -= 1
            self.labyrinth.active_player_number = active_player.get_object_id().number
            if kicked_players:
                self.labyrinth.send_msg(FIRE_SUCCESS_MSG
                                        + ', '.join(list(map(lambda player: player.user_id, kicked_players)))
                                        + '.', active_player.user_id)
            else:
                self.labyrinth.send_msg(FIRE_FAILURE_MSG, active_player.user_id)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return bool(active_player.states['count_of_bullets'])


class Bomb(LO):
    def __init__(self):
        self.new_at(self.turn_blow_up('up'), self.condition, BLOW_UP_UP)
        self.new_at(self.turn_blow_up('down'), self.condition, BLOW_UP_DOWN)
        self.new_at(self.turn_blow_up('left'), self.condition, BLOW_UP_LEFT)
        self.new_at(self.turn_blow_up('right'), self.condition, BLOW_UP_RIGHT)

    def turn_blow_up(self, direction):
        def blow_up():
            active_player = self.labyrinth.get_active_player()
            active_player.states['count_of_bombs'] -= 1

            current_location_id = active_player.get_parent_id()
            location_in_direction = self.field.get_neighbour_location(current_location_id, direction)
            if type(location_in_direction) is Wall:
                location_in_direction.break_wall(current_location_id, direction)
            # TODO: HURT_EVBD_IN_DIR
            # TODO: To code massage of blowing up.
        return blow_up

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return bool(active_player.states['count_of_bombs'])
