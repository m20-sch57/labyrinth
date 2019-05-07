from labyrinth_engine import Item
from labyrinth_objects.Vanilla.walls import Wall, Outside


class Bomb(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.BLOWUP_SUCCESS_MSG = settings['blowup_success_msg']['ru']
        self.BLOWUP_FAILURE_MSG = settings['blowup_failure_msg']['ru']
        self.BLOWUP_PROHIBITION_MSG = settings['blowup_prohibition_msg']['ru']
        self.CAN_HURT_SMB = settings['can_hurt_smb']
        self.BLOWUP_NOBODY_MSG = settings['blowup_nobody_msg']['ru']
        self.BLOWUP_ONEBODY_MSG = settings['blowup_onebody_msg']['ru']
        self.BLOWUP_MANYBODY_MSG = settings['blowup_manybody_msg']['ru']

        self.new_at(self.turn_blow_up('up'), self.condition, settings['blow_up_north']['ru'])
        self.new_at(self.turn_blow_up('down'), self.condition, settings['blow_up_south']['ru'])
        self.new_at(self.turn_blow_up('left'), self.condition, settings['blow_up_west']['ru'])
        self.new_at(self.turn_blow_up('right'), self.condition, settings['blow_up_east']['ru'])

        self.new_lbutton([settings['blow_up_north']['ru'], settings['blow_up_south']['ru'], 
            settings['blow_up_west']['ru'], settings['blow_up_east']['ru']], 
            'bomb.png', ['up.png', 'down.png', 'left.png', 'right.png'])

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
                self.labyrinth.send_msg(self.BLOWUP_SUCCESS_MSG, active_player)
            elif type(location_in_direction) is Outside:
                self.labyrinth.send_msg(self.BLOWUP_PROHIBITION_MSG, active_player)
            else:
                characters_in_direction = location_in_direction.get_children(lrtype=['player', 'creature'])
                if self.CAN_HURT_SMB and characters_in_direction:
                    for character in characters_in_direction:
                        health.hurt(character)

                    players_in_direction = location_in_direction.get_children(lrtype=['player'])
                    if len(players_in_direction) == 0:
                        msg = self.BLOWUP_NOBODY_MSG
                    elif len(players_in_direction) == 1:
                        msg = self.BLOWUP_ONEBODY_MSG
                    else:
                        msg = self.BLOWUP_MANYBODY_MSG
                    self.labyrinth.send_msg(msg
                                            + ', '.join(list(map(lambda pl: pl.get_username(),
                                                                 filter(lambda obj: obj.lrtype == 'player',
                                                                        players_in_direction))))
                                            + '.', active_player)
                else:
                    self.labyrinth.send_msg(self.BLOWUP_FAILURE_MSG, active_player)

        return blow_up

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        ammo = self.labyrinth.get_unique('ammo')
        return ammo.have('bomb', active_player)
