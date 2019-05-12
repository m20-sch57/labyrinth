from labyrinth_engine import Item


class Death(Item):
    def set_settings(self, settings, locations, items, creatures, players):
        self.DEATH_MSG = settings['death_msg']['ru']
        self.REVIVAL_MSG = settings['revival_msg']['ru']

        self.end_game_when_all_dead = settings['end_when_all_dead']
        self.DRAW_MSG = settings['draw_msg']['ru']

        self.death = {player: False for player in players}
        self.crt_death = {creature: False for creature in creatures}

        self.labyrinth.set_unique(self, 'death')

        self.set_name(settings['name'])

    def revive(self, body, revival_msg=None):
        if body.lrtype == 'player':
            self.death[body] = False
            self.labyrinth.send_msg(revival_msg or self.REVIVAL_MSG)
            body.revive()
        elif body.lrtype == 'creature':
            self.crt_death[body] = False
            body.revive()

    def revive_all(self, revival_msg=None):
        for player in self.death:
            self.death[player] = False
            self.labyrinth.send_msg(revival_msg or self.REVIVAL_MSG, player)
            player.revive()
        for creature in self.crt_death:
            self.crt_death[creature] = False
            creature.revive()

    def kill(self, body, death_msg=None):
        if body.lrtype == 'player':
            self.death[body] = True
            self.labyrinth.send_msg(death_msg or self.DEATH_MSG, body)
            body.die()
        elif body.lrtype == 'creature':
            self.crt_death[body] = True
            body.die()

    def kill_all(self, death_msg=None):
        for player in self.death:
            self.death[player] = True
            self.labyrinth.send_msg(death_msg or self.DEATH_MSG, player)
            player.die()
        for creature in self.crt_death:
            self.crt_death[creature] = True
            creature.die()

    def main(self):
        labyrinth = self.labyrinth
        now = labyrinth.active_player_number
        length = len(labyrinth.players_list)
        for i in range(len(self.labyrinth.players_list)):
            if self.death[labyrinth.players_list[(now + labyrinth.active_player_modifier) % length]]:
                labyrinth.active_player_modifier += 1
            else:
                break

        if all(self.death.values()) and self.end_game_when_all_dead:
            for player in self.death:
                self.labyrinth.send_msg(self.DRAW_MSG, player)
            self.labyrinth.end_game()
