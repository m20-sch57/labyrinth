from LabyrinthEngine.ui_buttons import CommonButton, DirectionButton, ListButton
from LabyrinthEngine.ui_status_bars import StringBar
from LabyrinthEngine.common_functions import get_attr_safe, append_safe
import json


class LabyrinthObject:
    """
    LabyrinthObject is class of objects that can be used by players at their turns
    """

    def new_at(self, function, condition_function, turn_name):
        """
        new available turn
        """
        append_safe(self, 'turn_set', turn_name, {'function': function, 'condition': condition_function})

    def new_button(self, turn, image):
        append_safe(self, 'button_set', CommonButton([turn], image))

    def new_dbutton(self, turns, image):
        append_safe(self, 'button_set', DirectionButton(turns, image))

    def new_lbutton(self, turns, image, turn_images):
        append_safe(self, 'button_set', ListButton(turns, image, turn_images))

    def new_status_bar(self, name, init_value):
        bar = StringBar(name, init_value)
        append_safe(self, 'bar_set', bar)
        return bar

    def set_parent(self, parent):
        if not isinstance(parent, LabyrinthObject):
            raise ValueError(
                'Invalid type of "parent" argument for LabyrinthObject.set_parent: ' + str(type(parent)))
        else:
            self.parent = parent

    def get_parent(self):
        return get_attr_safe(self, 'parent', None)

    def get_children(self, lrtype=['location', 'item', 'player', 'creature'], and_key=lambda x: True, or_key=lambda x: False):
        all_objs = self.labyrinth.get_all_objects()
        return set(filter(lambda obj: obj.get_parent() == self and (obj.lrtype in lrtype and and_key(obj) or or_key(obj)),
                        all_objs))

    def get_neighbour(self, direction):
        if self.lrtype != 'location':
            raise TypeError(
                'You can\'t get neighbour for object with lrtype ' + self.type)
        elif direction not in self.directions:
            raise ValueError(
                'Invalid "direction" argument for LabyrinthObject.get_neighbour: ' + str(direction))
        else:
            return self.directions[direction]

    def set_neighbour(self, direction, neighbour):
        if self.lrtype != 'location':
            raise TypeError(
                'You can\'t set neighbour for object with lrtype ' + self.type)
        elif not isinstance(neighbour, LabyrinthObject):
            raise ValueError(
                'Invalid "neighbour" argument for LabyrinthObject.set_neighbour: ' + str(neighbour))
        else:
            self.directions[direction] = neighbour

    def get_turns(self):
        return get_attr_safe(self, 'turn_set', {})

    def get_buttons(self):
        return get_attr_safe(self, 'button_set', [])

    def get_bars(self):
        return get_attr_safe(self, 'bar_set', [])

    @property
    def lrtype(self):
        return self._lrtype

    def main(self):
        """
        Основная функция объекта. Определяется здесь, чтобы потом не было ошибки при её вызове.
        """
        pass

    def set_settings(self, settings, *args):
        self.set_name(settings['name'])

    def get_name(self):
        return get_attr_safe(self, 'name', '')

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return '<{}: {}: {}>'.format(self.lrtype, self.__class__.__name__, self.get_name())

    def __repr__(self):
        return '<{}: {}: {}>'.format(self.lrtype, self.__class__.__name__, self.get_name())
