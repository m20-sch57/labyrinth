from LabyirnthObjects.DevelopersBacklog.consts import *
from LabyrinthEngine import Location, Item, Player, NPC


# TODO: To code DivineLightning.
# Item.
class DivineLightning(Item):
    def __init__(self):
        self.new_at(self.launch_lightning, self.condition, DL_LAUNCH_MSG)

    def launch_lightning(self):
        pass

    def condition(self):
        pass


class Flashlight(Item):
    pass
