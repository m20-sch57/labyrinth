from LabyrinthEngine import LabyrinthObject as LO


class Location(LO):
	_type = 'location'


class Item(LO):
	_type = 'item'


class Player(LO):
	'''
	Class of players of the game
	'''

	_type = 'player'

	def __init__(self, username):
		self.name = self.username = username

	def get_username(self):
		return self.username


class NPC(LO):
	_type = 'npc'
