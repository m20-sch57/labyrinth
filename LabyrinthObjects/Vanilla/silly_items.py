from LabyirnthConsts.Basic.CONSTS import *
from LabyrinthEngine.LTypes import Item


# Item.
class Treasure(Item):
    def __init__(self, is_true):
        self.is_true = is_true

        self.new_at(self.turn_take, self.take_condition, TAKE_TREASURE)
        self.new_at(self.turn_drop, self.drop_condition, DROP_TREASURE)

        self.new_lbutton([TAKE_TREASURE, DROP_TREASURE], 'res\\image.png', ['res\\image1', 'res\\image2'])

    def take(self, player):
        if WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
            self.initial_location = self.get_parent()
        self.set_parent(player)

    def drop(self):
        player = self.get_parent()
        if WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
            self.set_parent(self.initial_location)
        else:
            self.set_parent(player.get_parent())

    def turn_take(self):
        self.take(self.labyrinth.get_active_player())

    def turn_drop(self):
        self.drop()

    def take_condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent() == self.get_parent()

    def drop_condition(self):
        active_player = self.labyrinth.get_active_player()
        return CAN_PLAYER_DROP_TREASURE and self.get_parent() == active_player
