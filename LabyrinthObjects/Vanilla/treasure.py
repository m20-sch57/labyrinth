from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item


class Treasure(Item):
    def __init__(self):
        self.new_at(self.turn_take, self.take_condition, TAKE_TREASURE)
        self.new_at(self.turn_drop, self.drop_condition, DROP_TREASURE)

    def set_settings(self, settings, locations, *args):
        self.is_true = settings['is_true']
        self.set_parent(locations[settings['position']])
        self.set_name(settings['name'])

        self.WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED = settings['consts'].get(
            'will_treasure_returns_back_when_is_dropped') or WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED
        self.CAN_PLAYER_DROP_TREASURE = settings['consts'].get(
            'can_player_drop_treasure') or CAN_PLAYER_DROP_TREASURE

    def take(self, player):
        if self.WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
            self.initial_location = self.get_parent()
        self.set_parent(player)

    def drop(self):
        player = self.get_parent()
        if self.WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED:
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
        return self.CAN_PLAYER_DROP_TREASURE and self.get_parent() == active_player
