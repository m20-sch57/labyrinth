from LabyrinthObjects.Vanilla.consts import *
from LabyrinthEngine import Creature
from LabyrinthObjects.Vanilla.exit import Exit
from LabyrinthObjects.Vanilla.walls import borders


class Bear(Creature):
    def set_settings(self, settings, locations, *args):
        self.set_parent(locations[settings['position']])
        self.set_name(settings['name'])

        self.BEAR_MSG_ATTACK = settings['consts'].get('bear_msg_attack') or BEAR_MSG_ATTACK

    def move(self, direction):
        next_position = self.get_parent().get_neighbour(direction)
        if type(next_position) not in borders + [Exit]:
            self.set_parent(next_position)

    def main(self):
        health = self.labyrinth.get_unique('health')
        for player in self.get_parent().get_children(lrtype='player'):
            health.hurt(player)
            self.labyrinth.send_msg(self.BEAR_MSG_ATTACK, player)

        directions = {
            UP_TURN: 'up',
            DOWN_TURN: 'down',
            RIGHT_TURN: 'right',
            LEFT_TURN: 'left'
        }
        if self.labyrinth.get_turns(1)['turn'] in list(directions.keys()) and \
                self.labyrinth.get_active_player_username() == self.labyrinth.get_turns(1)['username']:
            self.move(directions[self.labyrinth.get_turns(1)['turn']])
