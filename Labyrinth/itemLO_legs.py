from Labyrinth.game import LabyrinthObject as LO

UP_TURN = 'Идти вверх'
DOWN_TURN = 'Идти вниз'
RIGHT_TURN = 'Идти вправо'
LEFT_TURN = 'Идти влево'

class Legs(LO):
	def __init__(self):
		super().__init__()
		self.new_at(self.up, condition_function = self.condition, turn_name = UP_TURN)
		self.new_at(self.down, condition_function = self.condition, turn_name = DOWN_TURN)
		self.new_at(self.right, condition_function = self.condition, turn_name = RIGHT_TURN)
		self.new_at(self.left, condition_function = self.condition, turn_name = LEFT_TURN)

	def up(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.field.up(active_player.get_parent_id().nomber))

	def down(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.field.down(active_player.get_parent_id().nomber))

	def right(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.field.right(active_player.get_parent_id().nomber))

	def left(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.field.left(active_player.get_parent_id().nomber))	

	def condition(self):
		return True