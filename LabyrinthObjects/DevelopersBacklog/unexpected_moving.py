from LabyirnthObjects.DevelopersBacklog.consts import *
from LabyrinthEngine import Location, Item, Player, NPC


class FlyingIsland(Location):
    def __init__(self):
        self.move_trigger = 1
        self.period_of_moving = DEFAULT_PERIOD_OF_MOVING
        self.bottom = FIBottom()

    def move(self):
        pass

    def main_after(self):
        self.move_trigger += 1
        if self.move_trigger == self.period_of_moving:
            self.move_trigger = 0
            self.move()


class FIBottom(Location):
    pass
