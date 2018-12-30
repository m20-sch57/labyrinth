class LabyrinthsList:
	'''
	Позволит хранить список игр в оперативной памяти

	room_id - это id комнаты в которой происходит игра
	'''
	def __init__(self):
		self.list = {}


	def get_labyrinth(room_id):
		return self.list[room_id]


	def add_labyrinth(room_id, labyrinth):
		if room_id in self.list:
			return False
		else:
			self.list[room_id] = labyrinth 
			return True


	def remove_labyrinth(room_id):
		if room_id in self.list:
			return False
		else:
			self.list.pop(room_id)
			return True
