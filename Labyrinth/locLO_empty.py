from Labyrinth.game import LabyrinthObject as LO

FIRST_ENTER_MSG = 'Ты попал в прямоугольную пустую комнату. Что ещё сказать?'
ENTER_MSG = 'И снова пусто'

class EmptyLocation(LO):
	used = {}
	def main(self):
		next_active_player = self.labyrinth.get_next_active_player()
		if next_active_player.get_parent_id() == self.object_id:
			if next_active_player.get_object_id().nomber in self.used:
				self.used[next_active_player.get_object_id().nomber] += 1
				self.labyrinth.send_msg(ENTER_MSG, next_active_player.user_id)
			else:
				self.used[next_active_player.get_object_id().nomber] = 1
				self.labyrinth.send_msg(FIRST_ENTER_MSG, next_active_player.user_id)