from LabyirnthConsts.Basic.CONSTS import *
from LabyrinthEngine import Location


# Location.
class Hole(Location):
    indulgence = {}

    def __init__(self):
        self.new_at(function=self.go_into_hole, condition_function=self.condition, turn_name=INTO_TURN)

        self.types_who_must_fall = TYPES_WHO_MUST_FALL_IN_IT
        self.and_who_must_fall = AND_WHO_MUST_FALL_IN_IT
        self.or_who_must_fall = OR_WHO_MUST_FALL_IN_IT

    def set_fall_to(self, fall_to):
        self.fall_to = fall_to

    def set_settings(self, settings, locations, items, npcs, players):
        self.set_fall_to(locations[settings['fall_to']])
        self.set_name(settings['name'])

    def main(self):
        for obj in self.labyrinth.get_all_objects():
            if obj in self.indulgence and obj.get_parent() != self.indulgence[obj]:
                self.indulgence[obj] = None

        for obj in self.get_children(labtype=self.types_who_must_fall,
                                     and_key=lambda obj: self.and_who_must_fall(obj) and
                                                         self.indulgence.get(obj, None) is None,
                                     or_key=self.or_who_must_fall):
            obj.set_parent(self.fall_to)
            if type(self.fall_to) is Hole:
                self.indulgence[obj] = self.fall_to
            else:
                self.indulgence[obj] = None

            if obj.type == 'player':
                self.labyrinth.send_msg(FALL_MSG, obj)

    def go_into_hole(self):
        active_player = self.labyrinth.get_active_player()
        active_player.set_parent(self.fall_to)
        if type(self.fall_to) is Hole:
            self.indulgence[active_player] = self.fall_to
        self.labyrinth.send_msg(TROUGH_HOLE_MSG, active_player)

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent() == self
