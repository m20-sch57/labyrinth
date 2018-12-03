from Labyrinth.game import LabyrinthObject as LO

FALL_MSG = 'К сожалению вы упали в яму. Мы не можем определить ваше новое местоположение'
ENTER_HOLE_MSG = 'Вы, наполняясь решимостью вошли в яму.'
ENTER_HOLE_TURN = 'Упасть в яму'

class HoleLocation(LO):
	flag = [False]
	def __init__(self, destination_object_id):
		super().__init__()
		self.destination_object_id = destination_object_id
		self.new_at(self.enter_hole, condition_function = self.condition, turn_name = ENTER_HOLE_TURN)

	def main(self):
		print(self.flag[0])
		active_player = self.labyrinth.get_active_player()
		next_active_player = self.labyrinth.get_next_active_player()
		if next_active_player.get_parent_id() == self.object_id and self.flag[0]:
			next_active_player.set_parent_id(self.destination_object_id)
			self.labyrinth.send_msg(FALL_MSG, next_active_player.user_id)
		if active_player.get_parent_id() != self.object_id:
			self.flag[0] = True
		else:
			self.flag[0] = False
		print(self.flag[0])

	def enter_hole(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.destination_object_id) 
		self.labyrinth.send_msg(ENTER_HOLE_MSG, active_player.user_id)

	def condition(self):
		return self.labyrinth.get_active_player().get_parent_id() == self.object_id 