from LabyrinthEngine import Location


class Arsenal(Location):
    def __init__(self):
        self.stayed = set()

    def set_settings(self, settings, *args):
        self.ENTER_MSG = settings['enter_msg']['ru']
        self.STAY_MSG = settings['stay_msg']['ru']

    def main(self):
        ammo = self.labyrinth.get_unique('ammo')
        for player in self.get_children(lrtype='player'):
            ammo.reset_all(player)
            if player in self.stayed:
                self.labyrinth.send_msg(self.STAY_MSG, player)
            else:
                self.labyrinth.send_msg(self.ENTER_MSG, player)
        self.stayed = set(self.get_children(lrtype='player'))
