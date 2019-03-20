from LabyrinthEngine.labyrinth import Labyrinth
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

	users = lrsave['users']
	labyrinth = load_lrmap(loadfile, savefile, users, lrseed=lrsave['seed'], loadseed=lrsave['loadseed'])

	for turn in lrsave['turns']:
		labyrinth.make_turn(turn['turn'])

	return labyrinth

def load_lrmap(loadfile, savefile, users, lrseed=random.randrange(sys.maxsize), loadseed=random.randrange(sys.maxsize)):
	random.seed(loadseed)

	with open('tmp\\' + loadfile + '.map.json', 'r', encoding='utf-8') as f:
		lrmap = json.load(f)

	Player = importlib.import_module('LabyrinthEngine').__dict__['Player']

	players = list(map(lambda username: Player(username), users))
	adjacence_list = lrmap['adjacence_list']
	settings = lrmap['settings']

	lrtypes = {
		'locations': [],
		'items': [],
		'creatures': [],
	}
	lrlists = lrtypes['locations'], lrtypes['items'], lrtypes['creatures']
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


	return Labyrinth(*lrlists, players, adjacence_list, settings, savefile, loadseed=loadseed, seed=lrseed)