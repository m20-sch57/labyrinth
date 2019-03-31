from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item
from LabyrinthObjects.Vanilla.walls import Wall, Outside


class Bomb(Item):
    def __init__(self):
        self.new_at(self.turn_blow_up('up'), self.condition, BLOW_UP_UP)
        self.new_at(self.turn_blow_up('down'), self.condition, BLOW_UP_DOWN)
        self.new_at(self.turn_blow_up('left'), self.condition, BLOW_UP_LEFT)
        self.new_at(self.turn_blow_up('right'), self.condition, BLOW_UP_RIGHT)

        self.new_lbutton([BLOW_UP_UP, BLOW_UP_DOWN, BLOW_UP_LEFT, BLOW_UP_RIGHT], 
            'bomb.png', ['up.png', 'down.png', 'left.png', 'right.png'])

    def set_settings(self, settings, locations, items, creatures, players):
        self.BLOW_UP_SUCCESS_MSG = settings.get('blowup_success_msg') or BLOW_UP_SUCCESS_MSG
        self.BLOW_UP_FAILURE_MSG = settings.get('blowup_failure_msg') or BLOW_UP_FAILURE_MSG
        self.BLOW_UP_PROHIBITION_MSG = settings.get('blowup_prohibition_msg') or BLOW_UP_PROHIBITION_MSG
        self.CAN_PLAYER_HURT_EVB_IN_DIRECTION = settings.get('can_hurt_smb') or \
                                                CAN_PLAYER_HURT_EVB_IN_DIRECTION
        self.BLOW_UP_NOT_PLAYERS_INJURING_MSG = settings.get('blowup_nobody_msg') or \
                                                BLOW_UP_NOT_PLAYERS_INJURING_MSG
        self.BLOW_UP_SINGLE_INJURING_MSG = settings.get('blowup_onebody_msg') or \
                                           BLOW_UP_SINGLE_INJURING_MSG
        self.BLOW_UP_MASSIVE_INJURING_MSG = settings.get('blowup_manybody_msg') or \
                                            BLOW_UP_MASSIVE_INJURING_MSG

    def turn_blow_up(self, direction):
        def blow_up():
            active_player = self.labyrinth.get_active_player()

            ammo = self.labyrinth.get_unique('ammo')
            ammo.spend('bomb', active_player)

            current_location = active_player.get_parent()
            location_in_direction = current_location.get_neighbour(direction)

            health = self.labyrinth.get_unique('health')

            if type(location_in_direction) is Wall:
                location_in_direction.break_wall()
                self.labyrinth.send_msg(self.BLOW_UP_SUCCESS_MSG, active_player)
            elif type(location_in_direction) is Outside:
                self.labyrinth.send_msg(self.BLOW_UP_PROHIBITION_MSG, active_player)
            else:
                characters_in_direction = location_in_direction.get_children(lrtype=['player', 'creature'])
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
                                                                 filter(lambda obj: obj.lrtype == 'player',
                                                                        players_in_direction))))
                                            + '.', active_player)
                else:
                    self.labyrinth.send_msg(self.BLOW_UP_FAILURE_MSG, active_player)

        return blow_up

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        ammo = self.labyrinth.get_unique('ammo')
        return ammo.have('bomb', active_player)
