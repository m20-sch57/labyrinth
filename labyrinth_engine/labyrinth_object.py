from labyrinth_engine.ui_buttons import CommonButton, DirectionButton, ListButton
from labyrinth_engine.ui_status_bars import StringBar


class LabyrinthObject:
    """
    LabyrinthObject is class of objects that can be used by players at their turns
    """

    labyrinth = None

    def __init__(self):
        self.turn_set = {}
        self.flags = set()
        self.button_set = []
        self.bar_set = []
        self.parent = None
        self.name = ''
        self._lrtype = ''

    # Предлагаемые игрокам ходы.
    def new_at(self, function, condition_function, turn_name):
        """
        new available turn
        """
        self.turn_set[turn_name] = {'function': function, 'condition': condition_function}

    def get_turns(self):
        return self.turn_set

    # Флаги.
    def add_flag(self, flag_name):
        self.flags.add(flag_name)

    def remove_flag(self, flag_name):
        self.flags.discard(flag_name)

    def have_flag(self, flag_name):
        return flag_name in self.flags

    # Кнопки.
    def new_button(self, turn, image):
        self.button_set.append(CommonButton([turn], image))

    def new_dbutton(self, turns, image):
        self.button_set.append(DirectionButton(turns, image))

    def new_lbutton(self, turns, image, turn_images):
        self.button_set.append(ListButton(turns, image, turn_images))

    def get_buttons(self):
        return self.button_set

    # Бары.
    def new_status_bar(self, name, init_value):
        bar = StringBar(name, init_value)
        self.bar_set.append(bar)
        return bar

    def get_bars(self):
        return self.bar_set

    # Родители, дети и т.д.
    def set_parent(self, parent):
        if not (isinstance(parent, LabyrinthObject) or parent is None):
            raise ValueError(
                'Invalid type of "parent" argument for LabyrinthObject.set_parent: ' + str(type(parent)))
        else:
            self.parent = parent

    def get_parent(self):
        return self.parent

    def get_children(self, lrtype=['location', 'item', 'player', 'creature'], class_names=[], flags=[], key=lambda x: True):
        return list(filter(lambda obj:
                           obj.lrtype in lrtype and
                           (type(obj).__name__ in class_names or not class_names) and
                           (all(obj.have_flag(flag) for flag in flags) or not flags) and
                           key(obj),
                           self.labyrinth.get_all_objects()))

    @property
    def lrtype(self):
        return self._lrtype

    def main(self):
        """
        Основная функция объекта. Определяется здесь, чтобы потом не было ошибки при её вызове.
        """
        pass

    def set_settings(self, settings, locations, items, creatures, players):
        pass

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return '<{}: {}: {}>'.format(self.lrtype, self.__class__.__name__, self.get_name())

    def __repr__(self):
        return '<{}: {}: {}>'.format(self.lrtype, self.__class__.__name__, self.get_name())
