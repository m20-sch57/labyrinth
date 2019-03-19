from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item

class Death(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.DEATH_MSG = settings.get('consts', {}).get('death_msg') or DEATH_MSG

        self.death = {player: False for player in players}
        self.crt_death = {creature: False for creature in creatures}

        self.labyrinth.set_unique_key(self, 'death')

        self.set_name(settings['name'])

    def revive(self, body):
        if body.lrtype == 'player':
            self.death[body] = False
        elif body.lrtype == 'creature':
            self.crt_death[body] = False

    def revive_all(self):
        for player in self.death:
            self.death[player] = False
        for creature in self.crt_death:
            self.crt_death[creature] = False

    def kill(self, body):
        if body.lrtype == 'player':
            self.death[body] = True
            self.labyrinth.send_msg(self.DEATH_MSG, body)
        elif body.lrtype == 'creature':
            self.crt_death[body] = True

    def kill_all(self):
        for player in self.death:
            self.death[player] = False
        for creature in self.crt_death:
            self.crt_death[creature] = False
