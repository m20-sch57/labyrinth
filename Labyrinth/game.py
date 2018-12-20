class LabyrinthObject:

	#new available turn
	def new_at(self, function, condition_function, turn_name):

		# если turn_set не определён для предмета, то self.turn_set вызовет ошибку,
		# и тогда выполнится self.turn_set = {}
		try:
			self.turn_set
		except:
			self.turn_set = {}

		if not turn_name in self.turn_set:
			self.turn_set[turn_name] = {'function': function, 'condition': condition_function}


	def get_object_id(self):
		return self.object_id
	def get_parent_id(self):
		return self.parent_id
	def set_object_id(self, new_id):
		self.object_id = new_id
	def set_parent_id(self, new_id):
		self.parent_id  = new_id

	def main(self):
		pass


class ObjectID:
	def __init__(self, object_type, object_number):
		self.type = object_type
		self.number= object_number
		# тип один из: location, item, player

	def __eq__(self ,other):
		return self.type == other.type and self.number == other.number


class Player(LabyrinthObject):
	def __init__(self, user_id):
		self.user_id = user_id
		self.turn_set = {} # На всякий случай

	def get_user_id(self):
		return self.user_id


class Field:
	def __init__(self, adjacence_list, locations_list, items_list, players_list):
		self.adjacence_list = adjacence_list
		self.locations_list = locations_list
		self.items_list = items_list
		self.players_list = players_list

		#раздаём всем id
		for i in range(len(self.locations_list)):
			self.locations_list[i].object_id = ObjectID('location', i)
		for i in range(len(self.items_list)):
			self.items_list[i].object_id = ObjectID('item', i)
		for i in range(len(self.players_list)):
			self.players_list[i].object_id = ObjectID('player', i)


	def get_neighbor_location(self, object_id, direction):
		return self.locations_list[self.adjacence_list[object_id.number][direction]].get_object_id()

	def get_object(self, object_id):
		lists = {
			'location': self.locations_list,
			'item': self.items_list,
			'player': self.players_list
		}
		return lists[object_id.type][object_id.number]


class Labyrinth:
	def __init__(self, field, send_msg_function):
		self.send_msg = send_msg_function
		self.field = field

		self.active_player_number = 0

	def ready(self):
		# Создаёт всем локациям артибуты field и labyrinth и turn_set
		for location in self.field.locations_list:
			location.labyrinth = self
			location.field = self.field
			try:
				location.turn_set
			except:
				location.turn_set = {}
		for item in self.field.items_list:
			item.labyrinth = self
			item.field = self.field
			try:
				item.turn_set
			except:
				item.turn_set = {}


	def make_turn(self, turn):
		to_do = []

		# В списке возможных ходов локаций и предметов ищем ход с именем turn
		for location in self.field.locations_list:
			if turn in location.turn_set and location.turn_set[turn]['condition']():
				to_do.append(location.turn_set[turn]['function'])
		for item in self.field.items_list:
			if turn in item.turn_set and item.turn_set[turn]['condition']():
				to_do.append(item.turn_set[turn]['function'])
		for function in to_do:
			function()

		# Запускаем для всех объектов main-функцию
		for location in self.field.locations_list:
			location.main()
		for item in self.field.items_list:
			item.main()

		# Делаем слудующего игрока активным
		self.active_player_number += 1
		self.active_player_number %= len(self.field.players_list)


	def add_player(self, user_id):
		self.field.add_player(Player(user_id), 0)


	def get_active_player(self):
		return self.field.players_list[self.active_player_number]
	def get_active_player_user_id(self):
		return self.get_active_player().user_id
	def get_next_active_player(self):
		return self.field.players_list[(self.active_player_number + 1)%len(self.field.players_list)]

	def get_active_player_ats(self):
		# Возвращает имена возможных ходов для активного игрока
		active_player_ats = []
		for location in self.field.locations_list:
			for turn in location.turn_set:
				if location.turn_set[turn]['condition']():
					active_player_ats.append(turn)
		for item in self.field.items_list:
			for turn in item.turn_set:
				if item.turn_set[turn]['condition']():
					active_player_ats.append(turn)		
		return active_player_ats
