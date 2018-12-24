from Labyrinth.LS_CONSTS import *
from Labyrinth.game import LabyrinthObject as LO, ObjectID


class Legs(LO):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function = self.condition, turn_name = UP_TURN)
        self.new_at(self.turn_move('down'), condition_function = self.condition, turn_name = DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function = self.condition, turn_name = RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function = self.condition, turn_name = LEFT_TURN)

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = self.field.get_object(self.field.get_neighbor_location(active_player.get_parent_id(),
                                                                                   direction))
            if type(next_position) is Wall:
                self.labyrinth.send_msg(WALL_MSG, active_player.get_user_id())
            else:
                active_player.set_parent_id(next_position.get_object_id())
        return move

    def condition(self):
        return True


class Bullet(LO):
    def __init__(self):
        self.counts_of_bul = {}

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
            while current_location.number not in met_locations:
                current_location = self.field.get_neighbor_location(current_location, direction)
                met_locations.add(current_location.number)
                kicked_players &= set(self.field.get_players_in_location(current_location))
            if not CAN_PLAYER_HURT_HIMSELF:
                kicked_players.discard(active_player.user_id)
            for player in kicked_players:
                if player.get_object_id().number not in self.field.hurt_players:
                    self.field.hurt_players.add(player.get_object_id().number)
                else:
                    ind = player.get_object_id().number
                    self.field.hurt_players.discard(ind)
                    player.set_object_id(ObjectID('dead_player', len(self.field.dead_players_list)))
                    self.field.dead_players_list.append(player)
                    self.field.players_list = self.field.players_list[:ind] + self.field.players_list[ind+1:]
                    for i in range(ind, len(self.field.players_list)):
                        self.field.players_list[i].get_object_id().number = i
                    player.set_parent_id(None)
                    self.labyrinth.number_of_players -= 1
            self.labyrinth.active_player_number = active_player.get_object_id().number
            if kicked_players:
                self.labyrinth.send_msg(FIRE_SUCCESS_MSG +
                    ', '.join(list(map(lambda player: player.user_id, kicked_players))) + '.', active_player.user_id)
            else:
                self.labyrinth.send_msg(FIRE_FAILURE_MSG, active_player.user_id)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        if active_player.get_object_id().number not in self.counts_of_bul:
            self.counts_of_bul[active_player.get_object_id().number] = INITIAL_COUNT_OF_BULLETS
        return bool(self.counts_of_bul[active_player.get_object_id().number])


# In progress...
# TODO: To code class of bombs
class Bomb(LO):
    def __init__(self):
        self.counts_of_bombs = {}

        self.new_at(self.turn_blow_up('up'), self.condition(), BLOW_UP_UP)
        self.new_at(self.turn_blow_up('down'), self.condition(), BLOW_UP_DOWN)
        self.new_at(self.turn_blow_up('left'), self.condition(), BLOW_UP_LEFT)
        self.new_at(self.turn_blow_up('right'), self.condition(), BLOW_UP_RIGHT)

    def turn_blow_up(self, direction):
        def blow_up():
            active_player = self.labyrinth.get_active_player()
            current_location = active_player.get_parent_id
            location_in_direction = self.field.get_neighbor_location(current_location, direction)
