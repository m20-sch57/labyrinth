from Labyrinth.game import LabyrinthObject as LO

UP_TURN = 'Идти вверх'
DOWN_TURN = 'Идти вниз'
RIGHT_TURN = 'Идти вправо'
LEFT_TURN = 'Идти влево'
WALL_MSG = 'Упсс. Стена'
ENTER_MSG = 'Ты в пустой комнате'


class EmptyLocation(LO):
	def main(self):
		next_active_player = self.labyrinth.get_next_active_player()
		active_player = self.labyrinth.get_active_player()

		if next_active_player.get_parent() == self:
			self.labyrinth.send_msg(ENTER_MSG, next_active_player)


class Legs(LO):
	def __init__(self):
		self.new_at(self.turn_move('up'), condition_function=self.condition, turn_name=UP_TURN)
		self.new_at(self.turn_move('down'), condition_function=self.condition, turn_name=DOWN_TURN)
		self.new_at(self.turn_move('right'), condition_function=self.condition, turn_name=RIGHT_TURN)
		self.new_at(self.turn_move('left'), condition_function=self.condition, turn_name=LEFT_TURN)

	def turn_move(self, direction):
		def move():
			active_player = self.labyrinth.get_active_player()
			next_position = active_player.get_parent().get_neighbour(direction)
			if type(next_position) is Wall:
				self.labyrinth.send_msg(WALL_MSG, active_player)
			else:
				active_player.set_parent(next_position)
		return move

	def condition(self):
		return True


class Wall(LO):
	pass
