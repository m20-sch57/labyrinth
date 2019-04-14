from LabyrinthEngine import Item


class Gun(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.CAN_HURT_IN_SAME_LOCATION = settings['can_hurt_in_same_location']
        self.CAN_HURT_HIMSELF = settings['can_hurt_himself']
        self.FIRE_SUCCESS_MSG = settings['fire_success_msg']['ru']
        self.FIRE_FAILURE_MSG = settings['fire_failure_msg']['ru']

        self.new_at(self.turn_fire('up'), self.condition, settings['fire_north']['ru'])
        self.new_at(self.turn_fire('down'), self.condition, settings['fire_south']['ru'])
        self.new_at(self.turn_fire('left'), self.condition, settings['fire_west']['ru'])
        self.new_at(self.turn_fire('right'), self.condition, settings['fire_east']['ru'])

        self.new_lbutton([settings['fire_north']['ru'], settings['fire_south']['ru'], 
            settings['fire_west']['ru'], settings['fire_east']['ru']], 
            'gun.png', ['up.png', 'down.png', 'left.png', 'right.png'])

    def turn_fire(self, direction):
        def fire():
            active_player = self.labyrinth.get_active_player()

            ammo = self.labyrinth.get_unique('ammo')
            ammo.spend('bullet', active_player)

            kicked_characters = set()
            met_locations = set()
            current_location = active_player.get_parent()

            health = self.labyrinth.get_unique('health')

            if self.CAN_HURT_IN_SAME_LOCATION:
                kicked_characters |= current_location.get_children(lrtype=['player', 'creature'])
                kicked_characters.discard(active_player)

            current_location = current_location.get_neighbour(direction)
            while current_location not in met_locations and not current_location.have_flag('border'):
                met_locations.add(current_location)
                kicked_characters |= current_location.get_children(lrtype=['player', 'creature'])
                current_location = current_location.get_neighbour(direction)

            if not self.CAN_HURT_HIMSELF:
                kicked_characters.discard(active_player)
            for character in kicked_characters:
                health.hurt(character)

            kicked_players = set(filter(lambda obj: obj.lrtype in ['player', 'dead_player'], kicked_characters))
            if kicked_characters:
                self.labyrinth.send_msg(self.FIRE_SUCCESS_MSG
                                        + ', '.join(list(map(lambda pl: pl.get_name(), kicked_characters)))
                                        + '.', active_player, 1)
            else:
                self.labyrinth.send_msg(self.FIRE_FAILURE_MSG, active_player, 1)
        return fire

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        ammo = self.labyrinth.get_unique('ammo')
        return ammo.have('bullet', active_player)
