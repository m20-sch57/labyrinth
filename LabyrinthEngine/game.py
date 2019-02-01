from LabyirnthConsts.Basic.CONSTS import *
from copy import copy
import json
import importlib
import random
import sys

class LabyrinthError(Exception):
	pass

class LabyrinthLoadError(LabyrinthError):
	def __init__(self, msg, file):
		self.msg = msg
		self.file = file

	def __str__(self):
		return 'File "{}"\n{}'.format(self.file, self.msg)

# TODO: understand errors. to continue the list of errors. Issue #44


def get_attr_safe(obj, attr, default_value):
	if hasattr(obj, attr):
		return obj.__dict__[attr]
	else:
		return default_value

def load_lrsave(loadfile, savefile):
	with open('tmp\\' + savefile + '.save.json', 'r', encoding='utf-8') as f:
		lrsave = json.load(f)

	if lrsave.get('loadseed') is not None:
		random.seed(lrsave['loadseed'])
	users = lrsave['users']
	labyrinth = load_lrmap(loadfile, savefile, users, seed=lrsave['seed'])

	for turn in lrsave['turns']:
		labyrinth.make_turn(turn['turn'])

	return labyrinth

def load_lrmap(loadfile, savefile, users):
	with open('tmp\\' + loadfile + '.map.json', 'r', encoding='utf-8') as f:
		lrmap = json.load(f)

	Player = importlib.import_module('LabyrinthEngine').__dict__['Player']

	players = list(map(lambda username: Player(username), users))
	adjacence_list = lrmap['adjacence_list']
	settings = lrmap['settings']

	lrtypes = {
		'locations': [],
		'items': [],
		'npcs': [],
	}
	lrlists = lrtypes['locations'], lrtypes['items'], lrtypes['npcs']
	for lrtype in lrtypes:
		if len(settings[lrtype]) != len(lrmap[lrtype]):
			raise LabyrinthLoadError('The number of {0} settings ({1}) does not match the number \
of {0} objects ({2})'.format(lrtype, len(settings[lrtype]), len(lrmap[lrtype])), loadfile + '.map.json')

	for lrtype in lrtypes:
		for obj in lrmap[lrtype]:
			lrtypes[lrtype].append(importlib.import_module(obj['module']).__dict__[obj['class_name']]())

	locs = lrmap['start_positions']['from']
	if lrmap['start_positions']['distribution'] == 'random':
		def get_start_position():
			not_used = locs[:]
			while True:
				while len(not_used) != 0:
					yield not_used.pop(random.randint(0, len(not_used) - 1))
				not_used = locs[:]
	elif lrmap['start_positions']['distribution'] == 'order':
		def get_start_position():
			index = 0
			while True:
				yield locs[index % len(locs)]
				index += 1
	elif lrmap['start_positions']['distribution'] == 'reverse_order':
		def get_start_position():
			index = -1
			while True:
				yield locs[index % len(locs)]
				index -= 1
	else:
		raise LabyrinthLoadError('Unexpected "distribution" value: "{}"'.format( \
			lrmap['start_positions']['distribution']), loadfile + '.map.json')
	position = get_start_position()

	for player in players:
		player.set_parent(lrtypes['locations'][next(position)])

	return Labyrinth(*lrlists, players, adjacence_list, settings, savefile)

class LabyrinthObject:
	'''
	LabyrinthObject is class of objects that can be used by players at their turns
	'''

	def new_at(self, function, condition_function, turn_name):
		'''
		new available turn
		'''

		if hasattr(self, 'turn_set'):
			self.turn_set[turn_name] = {
				'function': function, 'condition': condition_function}
		else:
			self.turn_set = {turn_name: {
				'function': function, 'condition': condition_function}}

	def set_parent(self, parent):
		if not isinstance(parent, LabyrinthObject):
			raise ValueError(
				'Invalid type of "parent" argument for LabyrinthObject.set_parent: ' + str(type(parent)))
		else:
			self.parent = parent

	def get_parent(self):
		return get_attr_safe(self, 'parent', None)

	def get_children(self, labtype=['location', 'item', 'player', 'NPC'], and_key=lambda x: True, or_key=lambda x: False):
		all_objs = self.labyrinth.get_all_objects()
		return set(filter(lambda obj: obj.get_parent() == self and (obj.type in labtype and and_key(obj) or or_key(obj)),
						all_objs))

	def get_neighbour(self, direction):
		if self.type != 'location':
			raise TypeError(
				'You can\'t get neighbour for object with type ' + self.type)
		elif direction not in self.directions:
			raise ValueError(
				'Invalid "direction" argument for LabyrinthObject.get_neighbour: {}\n \
Possible directions: {}'.format(str(direction), self.directions.keys))
		else:
			return self.directions[direction]

	def set_neighbour(self, direction, neighbour):
		if self.type != 'location':
			raise TypeError(
				'You can\'t set neighbour for object with type ' + self.type)
		elif not isinstance(neighbour, LabyrinthObject):
			raise ValueError(
				'Invalid "neighbour" argument for LabyrinthObject.set_neighbour: ' + str(neighbour))
		else:
			self.directions[direction] = neighbour

	def get_turn_set(self):
		return get_attr_safe(self, 'turn_set', {})

	@property
	def type(self):
		return self._type

	def main(self):
		'''
		Основная функция объекта. Определяется здесь, чтобы потом не было ошибки при её вызове.
		'''
		pass

	def set_settings(self, settings, *args):
		self.set_name(settings['name'])

	def get_name(self):
		return get_attr_safe(self, 'name', '')

	def set_name(self, name):
		self.name = name

	def __str__(self):
		return '<{}: {}: {}>'.format(self.type, self.__class__.__name__, self.get_name())

	def __repr__(self):
		return '<{}: {}: {}>'.format(self.type, self.__class__.__name__, self.get_name())


class Labyrinth:
	def __init__(self, locations, items, NPCs, players, adjacence_list, settings, savefile, save_mode=True, dead_players=[], seed=random.randrange(sys.maxsize)):
		random.seed(seed)
		self.seed = seed

		for i in range(len(locations)):
			locations[i].directions = {
				direction: locations[k] for direction, k in adjacence_list[i].items()}
		for player in players:
			player.states = copy(INITIAL_STATES)
			player.labyrinth = self
		for player in dead_players:
			player._type = 'dead_player'

		lrtypes = {
			'location': locations,
			'item': items,
			'npc': NPCs}
		lrlist = locations, items, NPCs, players

		for lrtype in lrtypes:
			for i in range(len(lrtypes[lrtype])):
				obj = lrtypes[lrtype][i]
				obj.labyrinth = self
				obj.set_settings(settings[obj.type + 's'][i], *lrlist)

		self.locations = set(locations)
		self.items = set(items)
		self.NPCs = set(NPCs)
		self.players_list = players
		self.dead_players = set(dead_players)

		self.to_send = {player.get_username(): [] for player in self.players_list}
		self.active_player_number = 0

		'''
		turns_log
		[{'player': first_player_name, 'turn': his_turn}, {'player': second_player_name, 'turn': his_turn}, ...]
		msgs_log
		{player_name: [first_msg, second_msg, ...]}
		'''
		self.turns_log = []
		self.msgs_log = {}

		# Временное решение.
		# Если True, то всё сохраняется в файл self.savefile
		self.save_mode = save_mode
		self.savefile = savefile

	def __str__(self):
		return '<labyrinth: {}>'.format(self.savefile)

	def send_msg(self, msg, player):
		self.to_send[player.get_username()].append(msg)

	def make_turn(self, turn):
		'''
		Вызвать эту функцию, если активный игрок сделал ход turn

		to_send: словарь сообщения для отправки.
		{username1: msg1, ... , username_n: msg_n}
		'''

		# обнуляем to_send
		self.to_send = {player.get_username(): [] for player in self.players_list}

		# В списке возможных ходов локаций и предметов ищем ход с именем turn
		# и запускаем действия найденных локаций и предметов
		to_do = []
		for obj in self.get_all_objects():
			if turn in obj.get_turn_set() and obj.get_turn_set()[turn]['condition']():
				to_do.append(obj.get_turn_set()[turn]['function'])
		for function in to_do:
			function()

		# Запускаем для всех объектов main-функцию
		for obj in self.get_all_objects():
			obj.main()

		# Делаем слудующего игрока активным
		self.active_player_number += 1
		self.active_player_number %= len(self.players_list)

		# обновляем лог ходов
		self.turns_log.append({'username': self.get_active_player_username(), 'turn': turn})
		# обновляем лог сообщений
		for username in self.to_send:
			if username in self.msgs_log:
				self.msgs_log[username].append(self.player_to_send(username))
			else:
				self.msgs_log[username] = [self.player_to_send(username)]
		# если save_mode == True, сохраняем всё в файл tmp\test.log
		if self.save_mode == True:
			self.save(self.savefile)

		# возвращаем все сообщения, которые нужно отправить
		return self.to_send

	def get_next_active_player(self):
		return self.players_list[(self.active_player_number + 1) % len(self.players_list)]

	def get_active_player(self):
		return self.players_list[self.active_player_number]

	def get_active_player_username(self):
		return self.get_active_player().get_username()

	def get_active_player_ats(self):
		'''
		Возвращает возможные для активного игрока ходы
		'''

		active_player_ats = []
		for obj in self.get_all_objects():
			for turn in obj.get_turn_set():
				if obj.get_turn_set()[turn]['condition']():
					active_player_ats.append(turn)

		return active_player_ats

	def get_all_objects(self):
		return self.locations | self.items | self.NPCs | set(self.players_list)

	def get_objects(self, lrtype=['location', 'item', 'player', 'npc'], and_key=lambda x: True, or_key=lambda x: False):
		return list(filter(lambda obj: obj.type in lrtype and and_key(obj) or or_key(obj), self.get_all_objects()))

	def player_to_send(self, username):
		return self.to_send[username]

	def save(self, savefile):
		save = {}
		save['seed'] = self.seed
		save['users'] = list(map(lambda user: user.get_username(), self.players_list))
		save['turns'] = self.turns_log
		with open('tmp\\' + savefile + '.save.json', 'w', encoding='utf-8') as f:
			json.dump(save, f, indent = 4, ensure_ascii=False)

	def get_msgs(self, username):
		'''
		Возвращает все сообщения отосланные игроку username
		'''

		if username in self.msgs_log:
			return self.msgs_log[username]
		else:
			return [] 

	def get_turns(self, number = None, username = None):
		'''
		Возвращает все ходы сделанные игроками
		Возвращает ходы сделанные только указанным игроками, если указан параметр username
		Возвращает ход под номером number с конца, если указан параметр number
		Например get_turns(1, 'Вася') вернёт последний ход Васи
		'''

		if username is None:
			if number is None:
				return self.turns_log
			else:
				return self.turns_log[-number]
		else:
			if number is None:
				return list(filter(lambda turn: turn['player'] in username, self.turns))
			else:
				return list(filter(lambda turn: turn['player'] in username, self.turns))[-number]
