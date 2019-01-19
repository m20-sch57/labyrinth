from LabyrinthEngine.game import LabyrinthObject as LabObj


class Location(LabObj):
	_type = 'location'


class Item(LabObj):
	_type = 'item'


class Player(LabObj):
	'''
	Class of players of the game
	'''

	_type = 'player'

	def __init__(self, username):
		self.name = self.username = username

	def get_username(self):
		return self.username


class NPC(LabObj):
	_type = 'NPC'
