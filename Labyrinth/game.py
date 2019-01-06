class LabyrinthObject:
	'''
	LabyrinthObject is class of objects that can be used by players at their turns
	'''

	def new_at(self, function, condition_function, turn_name):
		'''
		new available turn
		'''

		try:
			if turn_name not in self.turn_set:
				self.turn_set[turn_name] = {'function': function, 'condition': condition_function}
		except:
			self.turn_set = {turn_name: {'function': function, 'condition': condition_function}}

	def set_parent(self, parent):
		if not issubclass(type(parent), LabyrinthObject): 
			raise ValueError('Invalid type of "parent" argument for LabyrinthObject.set_parent: ' + str(type(parent)))
		else:
			self.parent = parent

	def get_parent(self):
		'''
		Если parent определён для данного объекта, вернёт его, иначе вернёт None
		'''
		try:
			return self.parent
		except:
			return None

	def get_neighbour(self, direction):
		if self.type != 'location':
			raise TypeError('You can\'t get neighbour for object with type ' + self.type)
		elif direction not in self.directions:
			raise ValueError('Invalid "direction" argument for LabyrinthObject.get_neighbour: ' + str(direction))
		else:
			return self.directions[direction]

	def set_neighbour(self, direction, neighbour):
		if self.type != 'location':
			raise TypeError('You can\'t set neighbour for object with type ' + self.type)
		elif not issubclass(type(neighbour), LabyrinthObject): 
			raise ValueError('Invalid "neighbour" argument for LabyrinthObject.set_neighbour: ' + str(neighbour))
		else:
			self.directions[direction] = neighbour

	def get_turn_set(self):
		try:
			return self.turn_set
		except:
			return {}

	@property
	def type(self):
		return self._type

	def main(self):
		'''
		Основная функция объекта. Определяется здесь, чтобы потом не было ошибки при её вызове.
		'''
		pass


class Player(LabyrinthObject):
	'''
	Class of players of the game
	'''

	def __init__(self, username):
		self.username = username
		self.turn_set = {}

	def get_username(self):
		return self.username


class Labyrinth:
	'''
	'''
	def __init__(self, locations_list, items_list, npcs_list, players_list, adjance_list):
		for i in range(len(locations_list)):
			locations_list[i].directions = {direction: locations_list[k] for direction, k in adjance_list[i].items()}
			locations_list[i]._type = 'location'
		for item in items_list:
			item._type = 'item'
		for npc in npcs_list:
			npc._type = 'npc'
		for player in players_list:
			player._type = 'player'

		for obj in locations_list + items_list + npcs_list + players_list:
			obj.labyrinth = self

		self.locations = set(locations_list)
		self.items = set(items_list)
		self.npcs = set(npcs_list)
		self.players_list = players_list

		self.to_send = {player.get_username(): '' for player in self.players_list}
		self.active_player_number = 0

	def send_msg(self, msg, player):
		self.to_send[player.get_username()] += (msg + ';')

	def make_turn(self, turn):
		'''
		Вызвать эту функцию, если активный игрок сделал ход turn

		to_send: словарь сообщения для отправки.
		{username1: msg1, ... , username_n: msg_n}
		'''

		# обнуляем to_send
		self.to_send = {player.get_username(): '' for player in self.players_list}

		# В списке возможных ходов локаций и предметов ищем ход с именем turn
		# и запускаем действия найденных локаций и предметов
		to_do = []
		for obj in self.locations | self.items | self.npcs | set(self.players_list):
			if turn in obj.get_turn_set() and obj.get_turn_set()[turn]['condition']():
				to_do.append(obj.get_turn_set()[turn]['function'])
		for function in to_do:
			function()

		# Запускаем для всех объектов main-функцию
		for obj in self.locations | self.items | self.npcs | set(self.players_list):
			obj.main()

		# Делаем слудующего игрока активным
		self.active_player_number += 1
		self.active_player_number %= len(self.players_list)

		# возвращаем все сообщения, которые нужно отправить, обнуляем to_send
		return self.to_send

	def get_next_active_player(self):
		return self.players_list[(self.active_player_number + 1) % len(self.players_list)]

	def get_active_player(self):
		return self.players_list[self.active_player_number]

	def get_active_player_username(self):
		return self.get_active_player().get_username()

	def get_active_player_ats(self):
		'''
		Возвращает возможные для активного игрока
		'''

		active_player_ats = []
		for obj in self.locations | self.items | self.npcs | set(self.players_list):
			for turn in obj.get_turn_set():
				if obj.get_turn_set()[turn]['condition']():
					active_player_ats.append(turn)

		return active_player_ats
