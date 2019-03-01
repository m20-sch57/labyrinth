from Vanilla.consts import *
from LabyrinthEngine import get_attr_safe
from LabyrinthEngine import Location, Item, Player, NPC
from Vanilla.move_and_bump import GlobalWall, Wall, Outside, borders


INITIAL_STATES['hurt'] = False
INITIAL_STATES['count_of_bullets'] = INITIAL_COUNT_OF_BULLETS
INITIAL_STATES['count_of_bombs'] = INITIAL_COUNT_OF_BOMBS


def hurt_player(self):
    active_player = self.labyrinth.get_active_player()

    for item in self.get_children():
        get_attr_safe(item, 'hurt_action', lambda: None)()

    if not self.states['hurt']:
        self.states['hurt'] = True
    else:
        ind = self.labyrinth.players_list.index(self)
        self._type = 'dead_player'
        self.labyrinth.dead_players.add(self)
        del self.labyrinth.players_list[ind]
        del self.parent
        self.labyrinth.send_msg(DEATH_MSG, self)
        if self != active_player:
            self.labyrinth.active_player_number = self.labyrinth.locations.index(active_player)
        else:
            self.labyrinth.active_player_number %= len(self.labyrinth.players_list)


def hurt_NPC(self):
    if not self.states['hurt']:
        self.states['hurt'] = True
    else:
        self.labyrinth.NPCs.discard(self)
        del self


def heal(self):
    self.states['hurt'] = False


Player.hurt = hurt_player
NPC.hurt = hurt_NPC
NPC.heal = Player.heal = heal


class Gun(Item):
    def __init__(self):
        self.new_at(self.turn_fire('up'), self.condition, FIRE_UP)
        self.new_at(self.turn_fire('down'), self.condition, FIRE_DOWN)
        self.new_at(self.turn_fire('left'), self.condition, FIRE_LEFT)
        self.new_at(self.turn_fire('right'), self.condition, FIRE_RIGHT)

    def set_settings(self, settings, locations, items, npcs, players):
        self.CAN_PLAYER_HURT_EVB_IN_SAME_LOC = settings['consts'].get('can_player_hurn_evb_in_same_loc') or CAN_PLAYER_HURT_EVB_IN_SAME_LOC
        self.CAN_PLAYER_HURT_HIMSELF = settings['consts'].get('can_player_hurt_himself') or CAN_PLAYER_HURT_HIMSELF
        self.FIRE_SUCCESS_MSG = settings['consts'].get('fire_success_msg') or FIRE_SUCCESS_MSG
        self.FIRE_FAILURE_MSG = settings['consts'].get('fire_failure_msg') or FIRE_FAILURE_MSG


    def turn_fire(self, direction):
        def fire():
            active_player = self.labyrinth.get_active_player()
            active_player.states['count_of_bullets'] -= 1

            kicked_characters = set()
            met_locations = set()
            current_location = active_player.get_parent()

            if self.CAN_PLAYER_HURT_EVB_IN_SAME_LOC:
                kicked_characters |= current_location.get_children(lrtype=['player', 'NPC'])
                kicked_characters.discard(active_player)

                current_location = current_location.get_neighbour(direction)
            while current_location not in met_locations and type(current_location) not in borders:
                met_locations.add(current_location)
                kicked_characters |= current_location.get_children(lrtype=['player', 'NPC'])
                current_location = current_location.get_neighbour(direction)

            if not self.CAN_PLAYER_HURT_HIMSELF:
                kicked_characters.discard(active_player)
            for character in kicked_characters:
                character.hurt()

            kicked_players = set(filter(lambda obj: obj.type == 'player', kicked_characters))
            if kicked_characters:
                self.labyrinth.send_msg(self.FIRE_SUCCESS_MSG
                                        + ', '.join(list(map(lambda pl: pl.get_username(), kicked_players)))
                                        + '.', active_player)
            else:
                self.labyrinth.send_msg(self.FIRE_FAILURE_MSG, active_player)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return bool(active_player.states['count_of_bullets'])


# Item.
class Bomb(Item):
    def __init__(self):
        self.new_at(self.turn_blow_up('up'), self.condition, BLOW_UP_UP)
        self.new_at(self.turn_blow_up('down'), self.condition, BLOW_UP_DOWN)
        self.new_at(self.turn_blow_up('left'), self.condition, BLOW_UP_LEFT)
        self.new_at(self.turn_blow_up('right'), self.condition, BLOW_UP_RIGHT)

    def set_settings(self, settings, locations, items, npcs, players):
        self.BLOW_UP_SUCCESS_MSG = settings['consts'].get('blow_up_success_msg') or BLOW_UP_SUCCESS_MSG
        self.BLOW_UP_FAILURE_MSG = settings['consts'].get('blow_up_failure_msg') or BLOW_UP_FAILURE_MSG
        self.BLOW_UP_PROHIBITION_MSG = settings['consts'].get('blow_up_prohibition_msg') or BLOW_UP_PROHIBITION_MSG
        self.CAN_PLAYER_HURT_EVB_IN_DIRECTION = settings['consts'].get('can_player_hurn_evb_in_derection') or CAN_PLAYER_HURT_EVB_IN_DIRECTION
        self.BLOW_UP_NOT_PLAYERS_INJURING_MSG = settings['consts'].get('blow_up_not_players_injuring_msg') or BLOW_UP_NOT_PLAYERS_INJURING_MSG
        self.BLOW_UP_SINGLE_INJURING_MSG = settings['consts'].get('blow_up_single_injuring_msg') or BLOW_UP_SINGLE_INJURING_MSG
        self.BLOW_UP_MASSIVE_INJURING_MSG = settings['consts'].get('blow_up_massive_injuring_msg') or BLOW_UP_MASSIVE_INJURING_MSG

    def turn_blow_up(self, direction):
        def blow_up():
            active_player = self.labyrinth.get_active_player()
            active_player.states['count_of_bombs'] -= 1

            current_location = active_player.get_parent()
            location_in_direction = current_location.get_neighbour(direction)
            if type(location_in_direction) is GlobalWall:
                location_in_direction.break_wall(current_location, direction)
                self.labyrinth.send_msg(self.BLOW_UP_SUCCESS_MSG, active_player)
            elif type(location_in_direction) is Wall:
                location_in_direction.break_wall()
                self.labyrinth.send_msg(self.BLOW_UP_SUCCESS_MSG, active_player)
            elif type(location_in_direction) is Outside:
                self.labyrinth.send_msg(self.BLOW_UP_PROHIBITION_MSG, active_player)
            else:
                characters_in_direction = location_in_direction.get_children(lrtype=['player', 'npc'])
                if self.CAN_PLAYER_HURT_EVB_IN_DIRECTION and characters_in_direction:
                    for character in characters_in_direction:
                        character.hurt()

                    players_in_direction = location_in_direction.get_children(lrtype=['player'])
                    if len(players_in_direction) == 0:
                        msg = self.BLOW_UP_NOT_PLAYERS_INJURING_MSG
                    elif len(players_in_direction) == 1:
                        msg = self.BLOW_UP_SINGLE_INJURING_MSG
                    else:
                        msg = self.BLOW_UP_MASSIVE_INJURING_MSG
                    self.labyrinth.send_msg(msg
                                            + ', '.join(list(map(lambda pl: pl.get_username(),
                                                                 filter(lambda obj: obj.type == 'player', players_in_direction))))
                                            + '.', active_player)
                else:
                    self.labyrinth.send_msg(self.BLOW_UP_FAILURE_MSG, active_player)
        return blow_up

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return bool(active_player.states['count_of_bombs'])


# Location.
class Arsenal(Location):
    def set_settings(self, settings, locations, items, npcs, players):
        self.INITIAL_COUNT_OF_BULLETS = settings['consts'].get('initial_count_of_bullets') or INITIAL_COUNT_OF_BULLETS
        self.INITIAL_COUNT_OF_BOMBS = settings['consts'].get('initial_count_of_bombs') or INITIAL_COUNT_OF_BOMBS
        self.set_name(settings['name'])

    def main(self):
        for player in self.get_children(lrtype='player'):
            player.states['count_of_bullets'] = self.INITIAL_COUNT_OF_BULLETS
            player.states['count_of_bombs'] = self.INITIAL_COUNT_OF_BOMBS


# Location.
class FirstAidPost(Location):
    def main(self):
        for player in self.get_children(lrtype='player'):
            player.heal()
