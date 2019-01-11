from Labyrinth.LS_CONSTS import *
from Labyrinth.game import LabyrinthObject as LabObj


class Location(LabObj):
	pass


class Item(LabObj):
	pass


class Player(LabObj):
	'''
	Class of players of the game
	'''

	def __init__(self, username):
		self.name = self.username = username

	def get_username(self):
		return self.username


class NPC(LabObj):
	pass
