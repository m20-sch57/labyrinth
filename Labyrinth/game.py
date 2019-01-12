class LogError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return 'LogError: ' + repr(self.msg)


class LabyrinthLogger:
	def __init__(self, filename):
		self.turns = []
		self.msgs = {}
		self.filename = filename
		self.save(filename)

	def save(self, file = None):
		if file is None:
			file = self.filename
		with open('tmp\\' + file + '.log', 'w') as f:
			for turn in self.turns:
				print('player: {}\nturn: {}'.format(turn['player'], turn['turn']), file=f)

	def load(self, file = None):
		if file is None:
			file = self.filename
		self.turns = []
		with open('tmp\\' + file + '.log', 'r') as f:
			player, turn = f.readline().rstrip(), f.readline().rstrip()
			while turn != '':
				if not (player.startswith('player: ') and turn.startswith('turn: ')):
					raise LogError('Invalid format in ' + file + '.log')
				self.update(player[len('player: '):], turn[len('turn: '):])
				player, turn = f.readline(), f.readline()

	def update_turn(self, player, turn):
		self.turns.append({'player': player, 'turn': turn})

	def update_msg(self, msgs):
		for player in msgs:
			if player in self.msgs:
				self.msgs[player] += msgs[player]
			else:
				self.msgs[player] = msgs[player]

	def get_all_msgs(self, player):
		if player in self.msgs:
			return self.msgs[player]
		else:
			return [] 

	def get_turns(self, player = None):
		if player == None:
			return self.turns
		else:
			return list(filter(lambda turn: turn['player'] == player, self.turns))

	def get_turn(self, *args):
		if len(args) == 0:
			return self.turns[-1]
		else:
			return self.turns[-int(args[0])]


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
				self.turn_set[turn_name] = {
					'function': function, 'condition': condition_function}
		except:
			self.turn_set = {turn_name: {
				'function': function, 'condition': condition_function}}

	def set_parent(self, parent):
		if not issubclass(type(parent), LabyrinthObject):
			raise ValueError(
				'Invalid type of "parent" argument for LabyrinthObject.set_parent: ' + str(type(parent)))
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
			raise TypeError(
				'You can\'t get neighbour for object with type ' + self.type)
		elif direction not in self.directions:
			raise ValueError(
				'Invalid "direction" argument for LabyrinthObject.get_neighbour: ' + str(direction))
		else:
			return self.directions[direction]

	def set_neighbour(self, direction, neighbour):
		if self.type != 'location':
			raise TypeError(
				'You can\'t set neighbour for object with type ' + self.type)
		elif not issubclass(type(neighbour), LabyrinthObject):
			raise ValueError(
				'Invalid "neighbour" argument for LabyrinthObject.set_neighbour: ' + str(neighbour))
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
	def __init__(self, locations, items, npcs, players, adjacence_list):
		for i in range(len(locations)):
			locations[i].directions = {
				direction: locations[k] for direction, k in adjacence_list[i].items()}
			locations[i]._type = 'location'
		for item in items:
			item._type = 'item'
		for npc in npcs:
			npc._type = 'npc'
		for player in players:
			player._type = 'player'

		for obj in locations + items + npcs + players:
			obj.labyrinth = self

		self.locations = set(locations)
		self.items = set(items)
		self.npcs = set(npcs)
		self.players_list = players

		self.to_send = {player.get_username(): '' for player in self.players_list}
		self.active_player_number = 0

		self.logger = LabyrinthLogger(filename = 'test2')
		self.logger.load(file = 'test')

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

		# возвращаем все сообщения, которые нужно отправить
		self.logger.update_turn(self.get_active_player_username(), turn)
		self.logger.save()
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

	def player_to_send(self, user_id):
		return self.to_send[user_id]
