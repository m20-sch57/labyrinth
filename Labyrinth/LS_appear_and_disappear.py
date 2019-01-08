from Labyrinth.LS_CONSTS import *
from Labyrinth.game_LR2 import LabyrinthObject as LO


INITIAL_STATES['is_fell'] = False


# TODO: To add setting MUST_PLAYER_FALL_IN_IT.
# Location.
class Hole(LO):
    def __init__(self, fall_to):
        self.fall_to = fall_to  # type is ObjectID
        self.new_at(function=self.go_into_hole, condition_function=self.condition, turn_name=INTO_TURN)

    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if active_player.get_parent_id() == self.get_object_id() and not active_player.states['is_fell']:
            active_player.set_parent_id(self.fall_to)
            if type(self.field.get_object(self.fall_to)) is Hole:
                active_player.states['is_fell'] = True
            self.labyrinth.send_msg(FALL_MSG, active_player.user_id)

        if type(self.field.get_object(next_active_player.get_parent_id())) is not Hole:
            next_active_player.states['is_fell'] = False
        for NPC in self.field.NPCs_list:
            if type(self.field.get_object(NPC.get_parent_id())) is not Hole:
                NPC.states['is_fell'] = False

    def be_swallowed(self, player_id):
        player = self.field.get_object(player_id)

        if player.get_parent_id() == self.get_object_id() and not player.states['is_fell']:
            player.set_parent_id(self.fall_to)
            if type(self.field.get_object(self.fall_to)) is Hole:
                player.states['is_fell'] = True

    def go_into_hole(self):
        active_player = self.labyrinth.get_active_player()
        active_player.set_parent_id(self.fall_to)
        self.labyrinth.send_msg(TROUGH_HOLE_MSG, active_player.user_id)

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent_id() == self.get_object_id()
