from Labyrinth.game import LabyrinthObject as LO

OUPS_MSG = 'Вы впечатались в стену. Очень удачно)'

class GlobalWall(LO):
	previouse_position = None
	def main(self):
		next_active_player = self.labyrinth.get_next_active_player()
		if next_active_player.get_parent_id() == self.object_id:
			self.labyrinth.send_msg(OUPS_MSG, next_active_player.user_id)
			next_active_player.set_parent_id(self.previouse_position)
		previouse_position = self.labyrinth.get_active_player().get_parent_id()