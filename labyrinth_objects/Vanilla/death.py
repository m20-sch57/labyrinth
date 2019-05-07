from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Item


class Death(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.DEATH_MSG = settings.get('consts', {}).get('death_msg') or DEATH_MSG
        self.REVIVAL_MSG = settings.get('consts', {}).get('revival_msg') or REVIVAL_MSG

        self.death = {player: False for player in players}
        self.crt_death = {creature: False for creature in creatures}

        self.labyrinth.set_unique_key(self, 'death')

        self.set_name(settings['name'])

    def revive(self, body, revival_msg=None):
        if body.lrtype == 'player':
            self.death[body] = False
            self.labyrinth.send_msg(revival_msg or self.REVIVAL_MSG)
        elif body.lrtype == 'creature':
            self.crt_death[body] = False

    def revive_all(self, revival_msg=None):
        for player in self.death:
            self.death[player] = False
            self.labyrinth.send_msg(revival_msg or self.REVIVAL_MSG, player)
        for creature in self.crt_death:
            self.crt_death[creature] = False

    def kill(self, body, death_msg=None):
        if body.lrtype == 'player':
            self.death[body] = True
            self.labyrinth.send_msg(death_msg or self.DEATH_MSG, body)
        elif body.lrtype == 'creature':
            self.crt_death[body] = True

    def kill_all(self, death_msg=None):
        for player in self.death:
            self.death[player] = True
            self.labyrinth.send_msg(death_msg or self.DEATH_MSG, player)
        for creature in self.crt_death:
            self.crt_death[creature] = True
