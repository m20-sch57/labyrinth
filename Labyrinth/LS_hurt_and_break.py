from Labyrinth.LS_CONSTS import *
from Labyrinth.game import LabyrinthObject as LO, Player
from Labyrinth.LS_move_and_bump import GlobalWall, Wall, Outside


INITIAL_STATES['hurt'] = False
INITIAL_STATES['count_of_bullets'] = 3
INITIAL_STATES['count_of_bombs'] = 3


def hurt_player(self):
    for item in self.get_everything_in_it():
        item.hurt_action()

    if not self.states['hurt']:
        self.states['hurt'] = True
    else:
        ind = self.labyrinth.players_list.index(self)
        self._type = 'dead_player'
        self.labyrinth.dead_players.add(self)
        del self.labyrinth.players_list[ind]
        del self.parent
        self.labyrinth.number_of_players -= 1
        self.labyrinth.send_msg(DEATH_MSG, self)


def hurt_npc(self):
    if not self.states['hurt']:
        self.states['hurt'] = True
    else:
        self.labyrinth.npcs.discard(self)
        del self


def heal(self):
    self.states['hurt'] = False


Player.hurt = hurt_player
NPC.hurt = hurt_npc
NPC.heal = Player.heal = heal


# Item.
# TODO: To fix bug: NPCs can be hurt and healed.
class Gun(LO):
    def __init__(self):
        self.new_at(self.turn_fire('up'), self.condition, FIRE_UP)
        self.new_at(self.turn_fire('down'), self.condition, FIRE_DOWN)
        self.new_at(self.turn_fire('left'), self.condition, FIRE_LEFT)
        self.new_at(self.turn_fire('right'), self.condition, FIRE_RIGHT)

    def turn_fire(self, direction):
        def fire():
            active_player = self.labyrinth.get_active_player()
            active_player.states['count_of_bullets'] -= 1

            kicked_players = set()
            met_locations = set()
            current_location = active_player.get_parent()

            if CAN_PLAYER_HURT_EVB_IN_SAME_LOC:
                kicked_players |= set(self.labyrinth.get_players_in_location(current_location))
                kicked_players.discard(active_player)

                current_location = current_location.get_neighbour(direction)
            while current_location not in met_locations and type(current_location) not in [GlobalWall, Wall, Outside]:
                met_locations.add(current_location)
                kicked_players |= set(self.labyrinth.get_players_in_location(current_location))
                current_location = current_location.get_neighbour(direction)

            if not CAN_PLAYER_HURT_HIMSELF:
                kicked_players.discard(active_player)
            for player in kicked_players:
                player.hurt()
            self.labyrinth.active_player_number = active_player.get_object_id().number

            if kicked_players:
                self.labyrinth.send_msg(FIRE_SUCCESS_MSG
                                        + ', '.join(list(map(lambda pl: pl.user_id, kicked_players)))
                                        + '.', active_player.user_id)
            else:
                self.labyrinth.send_msg(FIRE_FAILURE_MSG, active_player.user_id)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return bool(active_player.states['count_of_bullets'])


# Item.
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

            current_location = active_player.get_parent()
            location_in_direction = current_location.get_neighbour(direction)
            if type(location_in_direction) is GlobalWall:
                location_in_direction.break_wall(current_location, direction)
                self.labyrinth.send_msg(BLOW_UP_SUCCESS_MSG, active_player)
            elif type(location_in_direction) is Wall:
                location_in_direction.break_wall()
                self.labyrinth.send_msg(BLOW_UP_SUCCESS_MSG, active_player)
            elif type(location_in_direction) is Outside:
                self.labyrinth.send_msg(BLOW_UP_PROHIBITION_MSG, active_player)
            else:
                players_in_direction = self.labyrinth.get_players_in_location(location_in_direction)
                if CAN_PLAYER_HURT_EVB_IN_DIRECTION and players_in_direction:
                    if len(players_in_direction) == 1:
                        msg = BLOW_UP_SINGLE_INJURING_MSG
                    else:
                        msg = BLOW_UP_MASSIVE_INJURING_MSG
                    self.labyrinth.send_msg(msg
                                            + ', '.join(list(map(lambda pl: pl.user_id, players_in_direction)))
                                            + '.', active_player.user_id)
                    for player in players_in_direction:
                        player.hurt()
                else:
                    self.labyrinth.send_msg(BLOW_UP_FAILURE_MSG, active_player.user_id)
        return blow_up

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return bool(active_player.states['count_of_bombs'])


# Location.
class Arsenal(LO):
    def main(self):
        for player in self.labyrinth.get_players_in_location(self.get_object_id()):
            player.states['count_of_bullets'] = INITIAL_COUNT_OF_BULLETS
            player.states['count_of_bombs'] = INITIAL_COUNT_OF_BOMBS


# Location.
class FirstAidPost(LO):
    def main(self):
        for player in self.labyrinth.get_players_in_location(self.get_object_id()):
            player.heal()
