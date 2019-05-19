from labyrinth_engine import Creature


class Bear(Creature):
    def set_settings(self, settings, locations, *args):
        self.set_parent(locations[settings['position']])

        self.ATTACK_MSG = settings['attack_msg']['ru']

    def move(self, direction):
        next_position = self.get_parent().get_neighbour(direction)
        if not (next_position.have_flag('border') or next_position.have_flag('safe_zone')):
            self.set_parent(next_position)

    def main(self):
        health = self.labyrinth.get_unique('health')
        for player in self.get_parent().get_children(lrtype='player'):
            health.hurt(player)
            self.labyrinth.send_msg(self.ATTACK_MSG, player)

        directions = {
            'Идти вверх': 'up',
            'Идти вниз': 'down',
            'Идти вправо': 'right',
            'Идти влево': 'left'
        }
        if self.labyrinth.get_turns(1)['turn'] in directions and \
                self.labyrinth.get_active_player_username() == self.labyrinth.get_turns(1)['username']:
            self.move(directions[self.labyrinth.get_turns(1)['turn']])

    def die(self):
        self.labyrinth.creatures.discard(self)
