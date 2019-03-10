from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import get_attr_safe
from LabyrinthEngine import Location, Item, Player, NPC
from LabyrinthObjects.Vanilla.move_and_bump import GlobalWall, Wall, Outside, borders


class Ammo(Item):
    # def __init__(self):
    #     def resetallself():
    #         self.reset_all(self.labyrinth.get_active_player())
    #     self.new_at(resetallself, lambda: True, 'Восстановить патроны')

    def set_settings(self, settings, locations, items, npcs, players):
        self.MAX_BULLETS_COUNT = settings.get('max_bullets_count') or MAX_BULLETS_COUNT
        self.MAX_BOMBS_COUNT = settings.get('max_bombs_count') or MAX_BOMBS_COUNT

        self.INIT_BULLETS_COUNT = settings.get('init_bullets_count') or self.MAX_BULLETS_COUNT
        self.INIT_BOMBS_COUNT = settings.get('init_bombs_coount') or self.MAX_BOMBS_COUNT

        self.bullets = {player: self.INIT_BULLETS_COUNT for player in players}
        self.bombs = {player: self.INIT_BOMBS_COUNT for player in players}

        self.labyrinth.set_unique_key(self, 'ammo')

        self.set_name(settings['name'])


    def spend(self, ammo_type, player):
        if ammo_type == 'bullet':
            self.bullets[player] -= 1
            return self.bullets[player]
        elif ammo_type == 'bomb':
            self.bombs[player] -= 1
            return self.bombs[player]

    def have(self, ammo_type, player):
        if ammo_type == 'bullet':
            return self.bullets[player] > 0
        elif ammo_type == 'bomb':
            return self.bombs[player] > 0

    def reset(self, ammo_type, player):
        if ammo_type == 'bullet':
            self.bullets[player] = self.MAX_BULLETS_COUNT
        elif ammo_type == 'bomb':
            self.bombs[player] = self.MAX_BOMBS_COUNT

    def reset_all(self, player):
        self.bullets[player] = self.MAX_BULLETS_COUNT
        self.bombs[player] = self.MAX_BOMBS_COUNT


class Health(Item):
    # def __init__(self):
    #     def hurtself():
    #         self.hurt(self.labyrinth.get_active_player())
    #     self.new_at(hurtself, lambda: True, 'Ранить себя')
    #     def healself():
    #         self.heal(self.labyrinth.get_active_player())
    #     self.new_at(healself, lambda: True, 'Вылечиться')

    def set_settings(self, settings, locations, items, npcs, players):
        self.MAX_PLAYER_HEALTH = settings.get('max_player_health') or MAX_PLAYER_HEALTH
        self.MAX_NPC_HEALTH = settings.get('max_npc_health') or MAX_NPC_HEALTH

        self.hp = {player: self.MAX_NPC_HEALTH for player in players}
        self.npc_hp = {npc: self.MAX_NPC_HEALTH for npc in npcs}

        self.labyrinth.set_unique_key(self, 'health')

        self.set_name(settings['name'])

        self.DEATH_MSG = settings.get('consts', {}).get('death_msg') or DEATH_MSG


    def hurt(self, body):
        if body.lrtype == 'npc':
            self.npc_hp[body] -= 1
            self.labyrinth.NPCs.discard(body)

        elif body.lrtype == 'player':
            self.hp[body] -= 1

            if self.hp[body] == 0:
                index = self.labyrinth.players_list.index(body)
                del self.labyrinth.players_list[index]

                self.labyrinth.send_msg(self.DEATH_MSG, body)

    def heal(self, body):
        if body.lrtype == 'npc':
            self.npc_hp[body] = self.MAX_NPC_HEALTH
        elif body.lrtype == 'player':
            self.hp[body] = self.MAX_PLAYER_HEALTH


    # def hurt_player(self):
    #     active_player = self.labyrinth.get_active_player()

    #     for item in self.get_children():
    #         get_attr_safe(item, 'hurt_action', lambda: None)()

    #     if not self.states['hurt']:
    #         self.states['hurt'] = True
    #     else:
    #         ind = self.labyrinth.players_list.index(self)
    #         self._type = 'dead_player'
    #         self.labyrinth.dead_players.add(self)
    #         del self.labyrinth.players_list[ind]
    #         del self.parent
    #         self.labyrinth.send_msg(DEATH_MSG, self)
    #         if self != active_player:
    #             self.labyrinth.active_player_number = self.labyrinth.locations.index(active_player)
    #         else:
    #             self.labyrinth.active_player_number %= len(self.labyrinth.players_list)


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

            ammo = self.labyrinth.get_unique('ammo')
            ammo.spend('bullet', active_player)

            kicked_characters = set()
            met_locations = set()
            current_location = active_player.get_parent()

            health = self.labyrinth.get_unique('health')

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
                health.hurt(character)

            kicked_players = set(filter(lambda obj: obj.lrtype in ['player', 'dead_player'], kicked_characters))
            if kicked_characters:
                self.labyrinth.send_msg(self.FIRE_SUCCESS_MSG
                                        + ', '.join(list(map(lambda pl: pl.get_username(), kicked_players)))
                                        + '.', active_player)
            else:
                self.labyrinth.send_msg(self.FIRE_FAILURE_MSG, active_player)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        ammo = self.labyrinth.get_unique('ammo')
        return ammo.have('bullet', active_player)


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

            ammo = self.labyrinth.get_unique('ammo')
            ammo.spend('bomb', active_player)

            current_location = active_player.get_parent()
            location_in_direction = current_location.get_neighbour(direction)
            
            health = self.labyrinth.get_unique('health')

            if type(location_in_direction) is GlobalWall:
                location_in_direction.break_wall(current_location, direction)
                self.labyrinth.send_msg(self.BLOW_UP_SUCCESS_MSG, active_player, 1)
            elif type(location_in_direction) is Wall:
                location_in_direction.break_wall()
                self.labyrinth.send_msg(self.BLOW_UP_SUCCESS_MSG, active_player, 1)
            elif type(location_in_direction) is Outside:
                self.labyrinth.send_msg(self.BLOW_UP_PROHIBITION_MSG, active_player)
            else:
                characters_in_direction = location_in_direction.get_children(lrtype=['player', 'npc'])
                if self.CAN_PLAYER_HURT_EVB_IN_DIRECTION and characters_in_direction:
                    for character in characters_in_direction:
                        health.hurt(character)

                    players_in_direction = location_in_direction.get_children(lrtype=['player'])
                    if len(players_in_direction) == 0:
                        msg = self.BLOW_UP_NOT_PLAYERS_INJURING_MSG
                    elif len(players_in_direction) == 1:
                        msg = self.BLOW_UP_SINGLE_INJURING_MSG
                    else:
                        msg = self.BLOW_UP_MASSIVE_INJURING_MSG
                    self.labyrinth.send_msg(msg
                                            + ', '.join(list(map(lambda pl: pl.get_username(),
                                                                 filter(lambda obj: obj.lrtype == 'player', players_in_direction))))
                                            + '.', active_player)
                else:
                    self.labyrinth.send_msg(self.BLOW_UP_FAILURE_MSG, active_player)
        return blow_up

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        ammo = self.labyrinth.get_unique('ammo')
        return ammo.have('bomb', active_player)


class Arsenal(Location):
    def set_settings(self, settings, locations, items, npcs, players):
        self.INITIAL_COUNT_OF_BULLETS = settings['consts'].get('initial_count_of_bullets') or INITIAL_COUNT_OF_BULLETS
        self.INITIAL_COUNT_OF_BOMBS = settings['consts'].get('initial_count_of_bombs') or INITIAL_COUNT_OF_BOMBS
        self.set_name(settings['name'])

    def main(self):
        ammo = self.labyrinth.get_unique('ammo')
        for player in self.get_children(lrtype='player'):
            ammo.reset_all(player)


class FirstAidPost(Location):
    def main(self):
        health = self.labyrinth.get_unique('health')
        for player in self.get_children(lrtype='player'):
            health.heal(player)
