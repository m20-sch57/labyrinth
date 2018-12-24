from Labyrinth.game import LabyrinthObject as LO

UP_TURN = 'Идти вверх'
DOWN_TURN = 'Идти вниз'
RIGHT_TURN = 'Идти вправо'
LEFT_TURN = 'Идти влево'
WALL_MSG = 'Упсс. Стена'
FIRST_ENTER_MSG = 'Ты попал в прямоугольную пустую комнату. Что ещё сказать?'
ENTER_MSG = 'Опять нашёл пустую комнату?'

class EmptyLocation(LO):
    used = {}
    def main(self):
        next_active_player = self.labyrinth.get_next_active_player()
        active_player = self.labyrinth.get_active_player()

        if next_active_player.get_parent_id() == self.object_id:
            if next_active_player.get_object_id().number in self.used:
                self.used[next_active_player.get_object_id().number] += 1
                self.labyrinth.send_msg(ENTER_MSG, next_active_player.user_id)
            else:
                self.used[next_active_player.get_object_id().number] = 1
                self.labyrinth.send_msg(FIRST_ENTER_MSG, next_active_player.user_id)

class Legs(LO):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function = self.condition, turn_name = UP_TURN)
        self.new_at(self.turn_move('down'), condition_function = self.condition, turn_name = DOWN_TURN)
        self.new_at(self.turn_move('right'), condition_function = self.condition, turn_name = RIGHT_TURN)
        self.new_at(self.turn_move('left'), condition_function = self.condition, turn_name = LEFT_TURN)

    def turn_move(self, direction):
        def move():
            active_player = self.labyrinth.get_active_player()
            next_position = self.field.get_object(self.field.get_neighbor_location(active_player.get_parent_id(), direction))
            if type(next_position) is Wall:
                self.labyrinth.send_msg(WALL_MSG, active_player.get_user_id())
            else:
                active_player.set_parent_id(next_position.get_object_id())
        return move

    def condition(self):
        return True

class Wall(LO):
    pass