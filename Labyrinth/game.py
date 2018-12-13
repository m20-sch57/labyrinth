# LabyrinthObject is class of objects that can be used by players at their turns
class LabyrinthObject:
	def __init__(self):
		# Declaration of turn_set that'll contain TODO: contain what?
		self.turn_set = {}

	# new available turn
	def new_at(self, function, condition_function, turn_name):
		if not turn_name in self.turn_set:
			self.turn_set[turn_name] = {'function': function, 'condition': condition_function}

	# This two functions return object and parent's IDs.
	def get_object_id(self):
		return self.object_id
	def get_parent_id(self):
		return self.parent_id

	# This two function set object and parent's IDs to given value.
	def set_object_id(self, new_id):
		self.object_id.number = new_id
	def set_parent_id(self, new_id):
		self.parent_id.number  = new_id

	# TODO: understand what is this marvellous magic
	def main(self):
		pass

# Class for IDs. Nothing more.
class ObjectID:
	# Here object's type and number was declared in its ObjectID.
	# Every ID is type of object and its individual number among all objects with this type
	def __init__(self, object_type, object_number):
		self.type = object_type
		self.number= object_number
		# тип один из: location, item, player

	# This one helps to distinguish the differing and find the same objects.
	def __eq__(self ,other):
		# Obviously it needs only to compare types and IDs
		return self.type == other.type and self.number == other.number

# Class of players of the game.
class Player(LabyrinthObject):
	# On the level of program player is LabyrinthObject.
	def __init__(self, user_id):
		self.user_id = user_id

# Class of ALL field. There is only one field in every game.
class Field:
	def __init__(self):
		# TODO: what is it?
		self.adjacence_list = []
		# List of all locations in the game.
		self.locations_list = []
		# List of all items (but not players) in the game.
		self.items_list = []
		# List of all players in the game.
		self.players_list = []

	# This functions return location above, under, on the right and on the left (respectively) of given location.
	def up(self, id):
		return self.adjacence_list[id][0]
	def down(self, id):
		return self.adjacence_list[id][1]
	def right(self, id):
		return self.adjacence_list[id][2]
	def left(self, id):
		return self.adjacence_list[id][3]

	# This functions add player, item and location (respectively) in the game and return its ID in the game.
	# Functions themselves make ID for given object and append it to list of its type objects.
	def add_player(self, user_id, parent_id, parent_type='location'):
		P = Player(user_id)
		P.object_id = ObjectID('player', len(self.players_list))
		P.parent_id = ObjectID(parent_type, parent_id)
		self.players_list.append(P)
		return P.object_id.number

	def add_item(self, item, parent_id, parent_type='location'):
		item.object_id = ObjectID('item', len(self.items_list))
		item.parent_id = ObjectID(parent_type, parent_id)
		item.field = self
		self.items_list.append(item)
		return item.object_id.number

	def add_location(self, location, adjacence_locations):
		location.object_id = ObjectID('location', len(self.locations_list))
		location.field = self
		self.locations_list.append(location)
		self.adjacence_list.append(adjacence_locations)  #adjacence_locations - список номеров соседних локаций
		return location.object_id.number

	#TODO: make remove_object
	def remove_object(self, object_id):
		pass


	def object_with_id(self, object_id):
		lists = {
			'location': self.locations_list,
			'item': self.items_list,
			'player': self.players_list
		}
		return lists[object_id.type][object_id.number]

# Class of Labyrinths.
class Labyrinth:
	# Every Labyrinth is field and send_msg_function to send messages.
	def __init__(self, field, send_msg_function):
		self.send_msg = send_msg_function
		self.field = field

		self.active_player_number = 0
		self.number_of_players = 0

	def ready(self):
		# Создаёт всем локациям артибуты field и labyrinth со значением данного Labyrinth
		for location in self.field.locations_list:
			location.labyrinth = self
		for item in self.field.items_list:
			item.labyrinth = self

	def make_turn(self, turn):
		# В списке возможных ходов локаций и предметов ищем ход с именем turn
		# и запускаем действия найденных локаций и предметов.
		for location in self.field.locations_list:
			if turn in location.turn_set and location.turn_set[turn]['condition'](): # TODO: do condition function uses NOthing?!
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
		self.active_player_number %= self.number_of_players


	def add_player(self, user_id):
		self.field.add_player(user_id, 0)
		self.number_of_players += 1


	def get_active_player(self):
		return self.field.players_list[self.active_player_number]
	def get_next_active_player(self):
		return self.field.players_list[(self.active_player_number + 1) % len(self.field.players_list)]
	def get_active_player_ats(self):
		# Возвращает имена возможных ходов для активного игрока
		active_player_ats = []
		for location in self.field.locations_list: # TODO: There are a lot of passages of lists of location and items. Is it worth to make class of available turns?
			for turn in location.turn_set:
				if location.turn_set[turn]['condition']():
					active_player_ats.append(turn)
		for item in self.field.items_list:
			for turn in item.turn_set:
				if item.turn_set[turn]['condition']():
					active_player_ats.append(turn)		
		return active_player_ats
