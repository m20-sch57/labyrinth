from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Location


class FirstAidPost(Location):
    def main(self):
        health = self.labyrinth.get_unique('health')
        for player in self.get_children(lrtype='player'):
            health.heal(player)
