from labyrinth_engine.ui_buttons import CommonButton, DirectionButton, ListButton
from labyrinth_engine.ui_status_bars import StringBar


class LabyrinthObject:
    """
    LabyrinthObject is class of objects that can be used by players at their turns
    """

    labyrinth = None
    _lrtype = 'labyrinth_object'

    def __init__(self):
        self.triggers_set = []
        self.flags = {}
        self.button_set = []
        self.bar_set = []
        self.parent = None
        self.name = ''

    # Предлагаемые игрокам ходы.
    def new_at(self, event, function, condition=lambda: True):
        """
        new available turn
        """
        self.triggers_set.append({'event': event, 'function': function, 'condition': condition})
        event.add_trigger(self, condition, function)

    def get_triggers(self):
        return self.triggers_set

    # Флаги.
    def set_flag(self, flag_name, arg=None):
        self.flags[flag_name] = arg

    def delete_flag(self, flag_name):
        return self.flags.pop(flag_name, None)

    def have_flag(self, flag_name):
        return flag_name in self.flags

    def get_flag(self, flag_name, default=None):
        return self.flags.get(flag_name, default)

    # Кнопки.
    def new_button(self, event, name, image):
        self.button_set.append(CommonButton(self.labyrinth, [event], [name], image))

    def new_dbutton(self, events, names, image):
        self.button_set.append(DirectionButton(self.labyrinth, events, names, image))

    def new_lbutton(self, events, names, image, turn_images):
        self.button_set.append(ListButton(self.labyrinth, events, names, image, turn_images))

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
        return set(filter(lambda obj:
                           obj.get_parent() == self and 
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
