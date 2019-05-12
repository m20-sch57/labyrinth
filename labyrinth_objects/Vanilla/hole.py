from labyrinth_engine import Location


class Hole(Location):
    indulgence = {}

    def set_fall_to(self, fall_to):
        self.fall_to = fall_to

    def set_settings(self, settings, locations, items, creatures, players):
        self.set_fall_to(locations[settings['fall_to']])

        self.types_who_must_fall = settings['who_fall_in_it']
        self.GO_TROUGH_MSG = settings['go_through_msg']['ru']
        self.FALL_MSG = settings['fall_msg']['ru']

        self.new_at(self.go_into_hole, self.condition, settings['go_throught_turn']['ru'])

        # TODO: solve this problem (two buttins "fall into hole")
        if not 'kek' in self.__class__.__dict__:
            self.new_button(settings['go_throught_turn']['ru'], 'into_hole.png')
            self.__class__.kek = 'kek'

    def main(self):
        for obj in self.labyrinth.get_all_objects():
            if obj in self.indulgence and obj.get_parent() != self.indulgence[obj]:
                self.indulgence[obj] = None

        for obj in self.get_children(lrtype=self.types_who_must_fall,
                                     and_key=lambda obj: self.indulgence.get(obj, None) is None):
            obj.set_parent(self.fall_to)
            if type(self.fall_to) is Hole:
                self.indulgence[obj] = self.fall_to
            else:
                self.indulgence[obj] = None

            if obj.lrtype == 'player':
                self.labyrinth.send_msg(self.FALL_MSG, obj)

    def go_into_hole(self):
        active_player = self.labyrinth.get_active_player()
        active_player.set_parent(self.fall_to)
        if type(self.fall_to) is Hole:
            self.indulgence[active_player] = self.fall_to
        self.labyrinth.send_msg(self.GO_TROUGH_MSG, active_player)

    def condition(self):
        active_player = self.labyrinth.get_active_player()
        return active_player.get_parent() == self
