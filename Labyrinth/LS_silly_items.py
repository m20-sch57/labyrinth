from Labyrinth.LS_CONSTS import *
from Labyrinth.game_LR2 import LabyrinthObject as LO


# Item.
class Treasure(LO):
    def __init__(self, is_true):
        self.is_true = is_true

        self.new_at(self.turn_take, self.take_condition, TAKE_TREASURE)
        self.new_at(self.turn_drop, self.drop_condition, DROP_TREASURE)

    def take(self, player_id):
        player = self.field.get_object(player_id)
        self.set_parent_id(player_id)
        if WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
            self.initial_location = self.get_parent_id()
        player.in_hands.add(self.get_object_id())

    def drop(self):
        player = self.field.get_object(self.get_parent_id())
        if WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
            self.set_parent_id(self.initial_location)
        else:
            self.set_parent_id(player.get_parent_id())
        player.in_hands.discard(self.get_object_id)

    def turn_take(self):
        def take():
            player = self.labyrinth.get_active_player()
            player_id = player.get_object_id()
            self.set_parent_id(player_id)
            if WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
                self.initial_location = self.get_parent_id()
            player.in_hands.add(self.get_object_id())
        return take

    def turn_drop(self):
        def drop():
            player_id = self.get_parent_id()
            player = self.field.get_object(player_id)
            if WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
                self.set_parent_id(self.initial_location)
            else:
                self.set_parent_id(player.get_parent_id())
            player.in_hands.discard(self.get_object_id)
        return drop

    def take_condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent_id() == self.get_parent_id()

    def drop_condition(self):
        active_player_id = self.labyrinth.get_active_player_id()
        return CAN_PLAYER_DROP_TREASURE and self.get_parent_id() == active_player_id
