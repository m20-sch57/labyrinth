from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item
from LabyrinthObjects.Vanilla.walls import borders


class Gun(Item):
    def __init__(self):
        self.new_at(self.turn_fire('up'), self.condition, FIRE_UP)
        self.new_at(self.turn_fire('down'), self.condition, FIRE_DOWN)
        self.new_at(self.turn_fire('left'), self.condition, FIRE_LEFT)
        self.new_at(self.turn_fire('right'), self.condition, FIRE_RIGHT)

        self.new_lbutton([FIRE_UP, FIRE_DOWN, FIRE_LEFT, FIRE_RIGHT], 
            'gun.png', ['up.png', 'right.png', 'down.png', 'left.png'])


    def set_settings(self, settings, locations, items, creatures, players):
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
                kicked_characters |= current_location.get_children(lrtype=['player', 'creature'])
                kicked_characters.discard(active_player)

            current_location = current_location.get_neighbour(direction)
            while current_location not in met_locations and type(current_location) not in borders:
                met_locations.add(current_location)
                kicked_characters |= current_location.get_children(lrtype=['player', 'creature'])
                current_location = current_location.get_neighbour(direction)

            if not self.CAN_PLAYER_HURT_HIMSELF:
                kicked_characters.discard(active_player)
            for character in kicked_characters:
                health.hurt(character)

            kicked_players = set(filter(lambda obj: obj.lrtype in ['player', 'dead_player'], kicked_characters))
            if kicked_characters:
                self.labyrinth.send_msg(self.FIRE_SUCCESS_MSG
                                        + ', '.join(list(map(lambda pl: pl.get_username(), kicked_players)))
                                        + '.', active_player, 1)
            else:
                self.labyrinth.send_msg(self.FIRE_FAILURE_MSG, active_player, 1)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        ammo = self.labyrinth.get_unique('ammo')
        return ammo.have('bullet', active_player)