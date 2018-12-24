from Labyrinth.LS_CONSTS import *
from Labyrinth.game import LabyrinthObject as LO


class Hole(LO):
    is_not_fall = set()

    def __init__(self, fall_to):
        self.fall_to = fall_to # type is ObjectID
        self.new_at(function = self.go_into_hole, condition_function = self.condition, turn_name = INTO_TURN)

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if active_player.get_parent_id() == self.get_object_id() and active_player.get_object_id().number not in self.is_not_fall:
            active_player.set_parent_id(self.fall_to)
            if type(self.field.get_object(self.fall_to)) is Hole:
                self.is_not_fall.add(active_player.get_object_id().number)
            self.labyrinth.send_msg(FALL_MSG, active_player.user_id)

        if not type(self.field.get_object(next_active_player.get_parent_id())) is Hole:
            self.is_not_fall.discard(next_active_player.get_object_id().number)

    def go_into_hole(self):
        active_player = self.labyrinth.get_active_player()
        active_player.set_parent_id(self.fall_to)
        self.labyrinth.send_msg(TROUGH_HOLE_MSG, active_player.user_id)

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent_id() == self.get_object_id()