from labyrinth_engine import Location


class EmptyLocation(Location):
    def __init__(self):
        super().__init__()

        self.used = set()

    def set_settings(self, settings, locations, items, creatures, players):
        self.ENTER_MSG = settings['enter_msg']['ru']
        self.FIRST_ENTER_MSG = settings.get('first_enter_msg', {}).get('ru') or self.ENTER_MSG

        self.labyrinth.end_of_turn_event.add_trigger(self, self.main)

    def main(self):
        active_player = self.labyrinth.get_active_player()

        if active_player.get_parent() == self:
            if active_player in self.used:
                self.labyrinth.send_msg(self.ENTER_MSG, active_player, 5)
            else:
                self.used.add(active_player)
                self.labyrinth.send_msg(self.FIRST_ENTER_MSG, active_player, 5)
