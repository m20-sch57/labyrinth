import Labyrinth.game as lab

class SimpleLocation(lab.LabyrinthObject):
	def main(self):
		MSG = 'Ты оказался в простой локации'
		next_active_player = self.labyrinth.get_next_active_player()
		if next_active_player.get_parent_id() == self.object_id:
			self.labyrinth.send_msg(MSG, next_active_player.user_id)


class Legs(lab.LabyrinthObject):
	def __init__(self):
		self.new_at(self.up, condition_function = lambda: self.parent_id == self.labyrinth.get_active_player().get_object_id()
			, turn_name = 'Идти вверх')

	def up(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.field.up(active_player.get_object_id().nomber))

def send_msg_func(msg, user_id):
	print('[{}] - {}'.format(user_id, msg))

field = lab.Field()
MyLab = lab.Labyrinth(field, send_msg_func)

field.add_location(SimpleLocation(), [1, 1, 1, 1])
field.add_location(SimpleLocation(), [0, 0, 0, 0])
field.add_player(0, 0)
field.add_player(1, 0)
field.add_item(Legs(), 0, parent_type='player')
field.add_item(Legs(), 1, parent_type='player')

# print(MyLab.get_active_player_ats())
MyLab.ready()
while True:
	print(MyLab.get_active_player_ats())
	MyLab.make_turn(input())