from LabyirnthConsts.Basic.CONSTS import *
from LabyrinthEngine import NPC
from LabyrinthObjects.Vanilla.move_and_bump import borders
from LabyrinthObjects.Vanilla.go_out_and_rest import Exit


# NPC.
class Bear(NPC):
    def __init__(self):
        self.states = INITIAL_STATES

        self.new_at(self.turn_move('up'), condition_function=lambda: True, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=lambda: True, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=lambda: True, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=lambda: True, turn_name=LEFT_TURN)

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
        for player in self.get_parent().get_children(labtype='player'):
            player.hurt()
            self.labyrinth.send_msg(BEAR_MSG_ATTACK, player)
