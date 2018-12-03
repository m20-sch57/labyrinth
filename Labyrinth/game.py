class LabyrinthObject:
	def __init__(self):
		self.turn_set = []

	#new available turn
	def new_at(self, function, condition_function, turn_name):
		self.turn_set = {}
		if not turn_name in self.turn_set:
			self.turn_set[turn_name] = {'function': function, 'condition': condition_function}

	def get_object_id(self):
		return self.object_id
	def get_parent_id(self):
		return self.parent_id
	def set_object_id(self, new_id):
		self.object_id.number = new_id
	def set_parent_id(self, new_id):
		self.parent_id.number  = new_id

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


class Field:
	def __init__(self):
		self.adjacence_list = []
		self.locations_list = []
		self.items_list = []
		self.players_list = []

	def up(self, id):
		return self.adjacence_list[id][0]
	def down(self, id):
		return self.adjacence_list[id][1]
	def right(self, id):
		return self.adjacence_list[id][2]
	def left(self, id):
		return self.adjacence_list[id][3]


	def add_player(self, user_id, parent_id, parent_type='location'):
		P = Player(user_id)
		P.object_id = ObjectID('player', len(self.players_list))
		P.parent_id = ObjectID(parent_type, parent_id)
		self.players_list.append(P)
		return P.object_id.number

	def add_item(self, item, parent_id, parent_type='location'):
		item.object_id = ObjectID('item', len(self.items_list))
		item.parent_id = ObjectID(parent_type, parent_id)
		self.items_list.append(item)
		return item.object_id.number

	def add_location(self, location, adjacence_locations):
		location.object_id = ObjectID('location', len(self.locations_list))
		self.locations_list.append(location)
		self.adjacence_list.append(adjacence_locations)  #adjacence_locations - список номеров соседних локаций
		return location.object_id.number

	#TODO remove_object
	def remove_object(self, object_id):
		pass


	def object_with_id(self, object_id):
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
		# Создаёт всем локациям артибуты field и labyrinth 
		for location in self.field.locations_list:
			location.labyrinth = self
			location.field = self.field
		for item in self.field.items_list:
			item.labyrinth = self
			item.field = self.field

	def make_turn(self, turn):
		# В списке возможных ходов локаций и предметов ищем ход с именем turn
		for location in self.field.locations_list:
			if turn in location.turn_set and location.turn_set[turn]['condition']():
				location.turn_set[turn]['function']()
		for item in self.field.items_list:
			if turn in item.turn_set and item.turn_set[turn]['condition']():
				item.turn_set[turn]['function']()
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
