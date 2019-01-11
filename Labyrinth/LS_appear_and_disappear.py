from Labyrinth.LS_CONSTS import *
from Labyrinth.LS_fundamental_four import Location


INITIAL_STATES['is_fell'] = False


# TODO: To add setting MUST_PLAYER_FALL_IN_IT.
# Location.
class Hole(Location):
    is_not_fall = set()

    def __init__(self):
        self.new_at(function=self.go_into_hole, condition_function=self.condition, turn_name=INTO_TURN)

    def set_fall_to(self, fall_to):
        self.fall_to = fall_to

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if active_player.get_parent() == self and active_player not in self.is_not_fall:
            active_player.set_parent(self.fall_to)
            if type(self.fall_to) is Hole:
                self.is_not_fall.add(active_player)
            self.labyrinth.send_msg(FALL_MSG, active_player)

        if not type(next_active_player.get_parent()) is Hole:
            self.is_not_fall.discard(next_active_player)

    def go_into_hole(self):
        active_player = self.labyrinth.get_active_player()
        active_player.set_parent(self.fall_to)
        self.labyrinth.send_msg(TROUGH_HOLE_MSG, active_player)

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent() == self
