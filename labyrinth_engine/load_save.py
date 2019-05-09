from labyrinth_engine.labyrinth import Labyrinth
from labyrinth_engine.errors import LabyrinthLoadError
from labyrinth_engine.common_functions import from_module_name_to_path
import json
import importlib
import random
import sys


def load_save(save, _map):
	# если save - json-строка, то заменяем её на словарь
	if type(save) is str:
		save = json.loads(save)

	users = save['users']
	labyrinth = load_map(_map, users, seed=save['seed'], loadseed=save['loadseed'])

	for turn in save['turns']:
		labyrinth.make_turn(turn['turn'])

	return labyrinth

def load_map(_map, users, loadseed=random.randrange(sys.maxsize), **kwargs):
	# установили сид для загрузки карты.
	random.seed(loadseed)

	# если _map json-строка, то заменяем её на словарь
	if type(_map) is str:
		_map = json.loads(_map)

	# получили класс игрока
	Player = importlib.import_module('labyrinth_engine').__dict__['Player']
	# список игроков
	players = list(map(lambda username: Player(username), users))
	adjacence_list = _map['adjacence_list']
	settings = _map['settings']

	lrtypes = {
		'locations': [],
		'items': [],
		'creatures': [],
	}

	# пилим настройки
	for lrtype in lrtypes:
		# кол-во настроек для объектов должно совпадать с кол-вом объектов
		if len(settings[lrtype]) != len(_map[lrtype]):
			raise LabyrinthLoadError('The number of {0} settings ({1}) does not match the number \
                                      of {0} objects ({2})'.format(lrtype, len(settings[lrtype]), 
                                      len(lrmap[lrtype])))

		for i in range(len(_map[lrtype])):
			obj = _map[lrtype][i]
			# директория, в которой лежит файл с дефолтными настройками
			obj_dir = from_module_name_to_path(obj['module'])
			with open(obj_dir+'\\default_settings.json', 'r', encoding='utf-8') as f:
				# получаем дефолтные настройки для класса нашего объекта
				ds = json.load(f).get(obj['class_name'], {})
				# обновляем настройки из картыы дефолтными настройками
				ds.update(settings[lrtype][i])
				# сохраняем в словарь конечных настроек
				settings[lrtype][i] = ds


	# создаем объекты лабиринта
	for lrtype in lrtypes:
		for obj in _map[lrtype]:
			lrtypes[lrtype].append(importlib.import_module(obj['module']).__dict__[obj['class_name']]())

	# расставляем игроков
	# места, куда их можно ставить
	locs = _map['settings']['player']['start_positions']['from']
	# принцип расстановки
	distribution = _map['settings']['player']['start_positions']['distribution']
	if distribution == 'random':
		def get_start_position():
			not_used = locs[:]
			while True:
				while len(not_used) != 0:
					yield not_used.pop(random.randint(0, len(not_used) - 1))
				not_used = locs[:]
	elif distribution == 'order':
		def get_start_position():
			index = 0
			while True:
				yield locs[index % len(locs)]
				index += 1
	elif distribution == 'reverse_order':
		def get_start_position():
			index = -1
			while True:
				yield locs[index % len(locs)]
				index -= 1
	else:
		raise LabyrinthLoadError('Unexpected "distribution" value: "{}"'.format(
			_map['start_positions']['distribution']))
	position = get_start_position()

	for player in players:
		player.set_parent(lrtypes['locations'][next(position)])


	return Labyrinth(lrtypes['locations'], lrtypes['items'], lrtypes['creatures'], players, adjacence_list, 
					settings, loadseed=loadseed, **kwargs)
