class Event:
    def __init__(self, name=None):
        self.triggers = {}
        self.name = name

    def add_handler(self, obj, function, condition=lambda: True):
        triggers = self.triggers.get(obj, [])
        triggers.append({'condition': condition, 'function': function})
        self.triggers[obj] = triggers

    def del_handler(self, obj):
        del self.triggers[obj]

    def trigger(self):
        for obj in self.triggers:
            for trigger in self.triggers[obj]:
                if trigger['condition']():
                    trigger['function']()

    def __str__(self):
        return '<Event: {}>'.format(self.__class__.__name__) if self.name is not None else\
            '<Event: {}: [{}]>'.format(self.__class__.__name__, self.name)


class EndOfTurn(Event):
    pass


class MainEvent(Event):
    pass
