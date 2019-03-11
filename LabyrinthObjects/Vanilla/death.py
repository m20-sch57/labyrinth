from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item

class Death(Item):
    def reset(self, player):
        self.death[player] = False