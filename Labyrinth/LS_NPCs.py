from Labyrinth.LS_CONSTS import *
from Labyrinth.LS_fundamental_four import NPC
from Labyrinth.LS_move_and_bump import Outside, GlobalWall, Wall


# NPC.
class Bear(NPC):
    def __init__(self):
        self.states = INITIAL_STATES

        self.new_at(self.turn_move('up'), condition_function=self.condition, turn_name=UP_TURN)
        self.new_at(self.turn_move('down'), condition_function=self.condition, turn_name=DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function=self.condition, turn_name=RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function=self.condition, turn_name=LEFT_TURN)

    def turn_move(self, direction):
        def move():
            next_position = self.get_parent().get_neighbour(direction)
            if type(next_position) not in [GlobalWall, Wall, Outside]:
                self.set_parent(next_position)
        return move

    def condition(self):
        return True

    def main(self):
        for player in self.labyrinth.get_players_in_location(self.get_parent()):
            player.hurt()
