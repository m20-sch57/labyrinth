from LabyrinthEngine import Location


class Arsenal(Location):
    def main(self):
        ammo = self.labyrinth.get_unique('ammo')
        for player in self.get_children(lrtype='player'):
            ammo.reset_all(player)
