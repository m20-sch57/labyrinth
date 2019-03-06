from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import NPC
from LabyrinthObjects.Vanilla.move_and_bump import borders
from LabyrinthObjects.Vanilla.go_out_and_rest import Exit


class Bear(NPC):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function=lambda: True, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=lambda: True, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=lambda: True, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=lambda: True, turn_name=LEFT_TURN)

    def set_settings(self, settings, locations, *args):
        self.set_parent(locations[settings['position']])
        self.set_name(settings['name'])

        self.BEAR_MSG_ATTACK = settings['consts'].get('bear_msg_attack') or BEAR_MSG_ATTACK

    def turn_move(self, direction):
        def move():
            next_position = self.get_parent().get_neighbour(direction)
            if type(next_position) not in borders + [Exit]:
                self.set_parent(next_position)
        return move

    def move(self, direction):
        next_position = self.get_parent().get_neighbour(direction)
        if type(next_position) not in borders + [Exit]:
            self.set_parent(next_position)

    def main(self):
        health = self.labyrinth.get_unique('health')
        for player in self.get_parent().get_children(lrtype='player'):
            health.hurt(player)
            self.labyrinth.send_msg(self.BEAR_MSG_ATTACK, player)
