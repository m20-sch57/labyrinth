from labyrinth_objects.DevelopersBacklog.consts import *
from labyrinth_engine import Location, Item, Player, Creature


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
