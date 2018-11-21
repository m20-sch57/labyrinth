def new_ams(condition_function, move_name):
	def decorator(self, function):
		def wrapper(self):
			if condition_function():
				function(self)
			else:
				pass
		self.object_move_set.append(wrapper)
		return function
	return decorator

class Field:
	def __init__(self, field):
		pass

class LabyrinthObject:
	def __init__(self, send_msg_function):
		self.send_msg = send_msg_function
		self.object_move_set = []

class Labyrinth:
	def __init__(self, room, send_msg_function):
		self.send_msg_function = send_msg_function
		self.field = room[0]
		self.user_id_list = room[1] #список user_id всех пользователей комнаты

		self.set_active_player(self.user_id_list[0])

	def make_turn(self, turn):
		pass

	def get_active_player_user_id(self):
		return self.active_player_user_id

	def set_active_player(self, user_id):
		if user_id in self.user_id_list:
			self.active_player_user_id = user_id
		else:
			raise ValieError('no user with user_id' + user_id)

	def get_active_player_ams(self):
		pass