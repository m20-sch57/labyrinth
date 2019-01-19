from random import choice
from LabyirnthConsts.Basic.CONSTS import *
from LabyrinthEngine.LTypes import Location


# Location.
class Exit(Location):
	def __init__(self):
		self.must_be_here = set()

	def main(self):
		now_here = self.get_children(['player'])
		for player in now_here - self.must_be_here:
			self.labyrinth.send_msg(EXIT_GREETING_MSG, player)
		for player in now_here & self.must_be_here:
			self.labyrinth.send_msg(choice(EXIT_PRESENCE_MSGS), player)
		self.must_be_here = now_here