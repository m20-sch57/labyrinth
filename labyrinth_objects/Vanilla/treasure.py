from labyrinth_engine import Item, Event


class Treasure(Item):
    def set_settings(self, settings, locations, *args):
        self.is_true = settings['is_true']
        self.set_parent(locations[settings['position']])

        self.RETURNS_BACK_WHEN_IS_DROPPED = settings['returns_back_when_is_dropped']
        self.CAN_PLAYER_DROP_TREASURE = settings['can_player_drop_treasure']
        self.UNDERFOOT_MSG = settings['underfoot_msg']['ru']

        take_event = Event(settings['take_turn']['ru'])
        drop_event = Event(settings['drop_turn']['ru'])
        self.new_at(take_event, self.turn_take, self.take_condition)
        self.new_at(drop_event, self.turn_drop, self.drop_condition)

        self.new_button(take_event, settings['take_turn']['ru'], 'treasure_up.png')
        self.new_button(drop_event, settings['drop_turn']['ru'], 'drop_treasure.png')

        if self.is_true:
            self.set_flag('true_tres')

        self.labyrinth.end_of_turn_event.add_trigger(self, self.main)

    def take(self, player):
        if self.RETURNS_BACK_WHEN_IS_DROPPED:
            self.initial_location = self.get_parent()
        self.set_parent(player)

    def drop(self):
        player = self.get_parent()
        if self.RETURNS_BACK_WHEN_IS_DROPPED:
            self.set_parent(self.initial_location)
        else:
            self.set_parent(player.get_parent())

    def turn_take(self):
        self.take(self.labyrinth.get_active_player())

    def turn_drop(self):
        self.drop()

    def take_condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent() == self.get_parent()

    def drop_condition(self):
        active_player = self.labyrinth.get_active_player()
        return self.CAN_PLAYER_DROP_TREASURE and self.get_parent() == active_player

    def main(self):
        if self.parent.lrtype == 'location':
            for player in self.parent.get_children('player'):
                self.labyrinth.send_msg(self.UNDERFOOT_MSG, player)
