from labyrinth_engine import Item


class Legs(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.BORDER_MSG = settings['border_msg']['ru']

        self.new_at(self.turn_move('up'), lambda: True, settings['go_north']['ru'])
        self.new_at(self.turn_move('down'), lambda: True, settings['go_south']['ru'])
        self.new_at(self.turn_move('left'), lambda: True, settings['go_west']['ru'])
        self.new_at(self.turn_move('right'), lambda: True, settings['go_east']['ru'])

        self.new_lbutton([settings['go_north']['ru'], settings['go_south']['ru'], 
            settings['go_west']['ru'], settings['go_east']['ru']], 'leg.png', 
            ['up.png', 'down.png', 'left.png', 'right.png'])

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = active_player.get_parent().get_neighbour(direction)
            if next_position.have_flag('border'):
                self.labyrinth.send_msg(self.BORDER_MSG, active_player, 1)
            else:
                active_player.set_parent(next_position)

        return move
