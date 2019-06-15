from labyrinth_engine import Item, unique


@unique('death')
class Death(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.DEATH_MSG = settings['death_msg']['ru']
        self.REVIVAL_MSG = settings['revival_msg']['ru']

        self.end_game_when_all_dead = settings['end_when_all_dead']
        self.DRAW_MSG = settings['draw_msg']['ru']

        self.death = {player: False for player in players}
        self.crt_death = {creature: False for creature in creatures}

    def revive(self, body, revival_msg=None):
        if body.lrtype == 'player':
            self.death[body] = False
            self.labyrinth.send_msg(revival_msg or self.REVIVAL_MSG)
            if hasattr(body, 'revive'):
                body.revive()
        elif body.lrtype == 'creature':
            self.crt_death[body] = False
            if hasattr(body, 'revive'):
                body.revive()

    def revive_all(self, revival_msg=None):
        for player in self.death:
            self.death[player] = False
            self.labyrinth.send_msg(revival_msg or self.REVIVAL_MSG, player)
            if hasattr(player, 'revive'):
                player.revive()
        for creature in self.crt_death:
            self.crt_death[creature] = False
            if hasattr(creature, 'revive'):
                creature.revive()

    def kill(self, body, death_msg=None):
        if body.lrtype == 'player':
            self.death[body] = True
            self.labyrinth.send_msg(death_msg or self.DEATH_MSG, body)
            if hasattr(body, 'die'):
                body.die()
        elif body.lrtype == 'creature':
            self.crt_death[body] = True
            if hasattr(body, 'die'):
                body.die()

    def kill_all(self, death_msg=None):
        for player in self.death:
            self.death[player] = True
            self.labyrinth.send_msg(death_msg or self.DEATH_MSG, player)
            if hasattr(player, 'die'):
                player.die()
        for creature in self.crt_death:
            self.crt_death[creature] = True
            if hasattr(creature, 'die'):
                creature.die()

    def main(self):
        if all(self.death.values()) and self.end_game_when_all_dead:
            for player in self.death:
                self.labyrinth.send_msg(self.DRAW_MSG, player)
            self.labyrinth.end_game()
