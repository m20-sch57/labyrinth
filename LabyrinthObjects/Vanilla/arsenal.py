from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Location


class Arsenal(Location):
    def set_settings(self, settings, locations, items, creatures, players):
        self.INITIAL_COUNT_OF_BULLETS = settings['consts'].get('initial_count_of_bullets') or INITIAL_COUNT_OF_BULLETS
        self.INITIAL_COUNT_OF_BOMBS = settings['consts'].get('initial_count_of_bombs') or INITIAL_COUNT_OF_BOMBS
        self.set_name(settings['name'])

    def main(self):
        ammo = self.labyrinth.get_unique('ammo')
        for player in self.get_children(lrtype='player'):
            ammo.reset_all(player)
