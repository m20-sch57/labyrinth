from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item
from LabyrinthObjects.Vanilla.walls import borders


class Legs(Item):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function=lambda: True, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=lambda: True, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=lambda: True, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=lambda: True, turn_name=LEFT_TURN)

        self.new_lbutton([UP_TURN, RIGHT_TURN, DOWN_TURN, LEFT_TURN], 'leg.png', ['up.png', 'right.png', 'down.png', 'left.png'])

    def set_settings(self, settings, locations, items, creatures, players):
        self.WALL_MSG = settings['consts'].get('wall_msg') or WALL_MSG

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = active_player.get_parent().get_neighbour(direction)
            if type(next_position) in borders:
                self.labyrinth.send_msg(self.WALL_MSG, active_player, 1)
            else:
                active_player.set_parent(next_position)

        return move
