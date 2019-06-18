from labyrinth_engine import Item, Event


class Walk(Event):
    def __init__(self, direction, name=None):
        super().__init__(name)
        self.direction = direction

    def __str__(self):
        return '<Event: {}: {}>'.format(self.__class__.__name__, self.direction) if self.name is not None else\
            '<Event: {}: {}: [{}]>'.format(self.__class__.__name__, self.direction, self.name)


class Legs(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.BORDER_MSG = settings['border_msg']['ru']
        self.SUCCESS_MSG = settings['success_msg']['ru']

        up_event = Walk('up', settings['go_north']['ru'])
        down_event = Walk('down', settings['go_south']['ru'])
        left_event = Walk('left', settings['go_west']['ru'])
        right_event = Walk('right', settings['go_east']['ru'])
        self.new_at(up_event, self.turn_move('up'))
        self.new_at(down_event, self.turn_move('down'))
        self.new_at(left_event, self.turn_move('left'))
        self.new_at(right_event, self.turn_move('right'))

        self.new_lbutton([up_event, down_event, left_event, right_event],
                         [settings['go_north']['ru'], settings['go_south']['ru'],
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
                self.labyrinth.send_msg(self.SUCCESS_MSG, active_player, 1)

        return move
