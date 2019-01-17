from LabyirnthConsts.Basic.CONSTS import *
from LabyrinthEngine.LTypes import NPC
from LabyrinthObjects.Vanilla.move_and_bump import borders


# NPC.
class Bear(NPC):
    def __init__(self):
        self.states = INITIAL_STATES

    def move(self, direction):
        next_position = self.get_parent().get_neighbour(direction)
        if type(next_position) not in borders:

    def main(self):
        for player in self.get_parent().get_children(types='player'):
            player.hurt()
