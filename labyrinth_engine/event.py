class Event:
    def __init__(self):
        self.triggers = {}

    def add_trigger(self, obj, condition, function):
        self.triggers[obj] = {'condition': condition, 'function': function}

    def del_trigger(self, obj):
        del self.triggers[obj]

    def trigger(self):
        for obj in self.triggers:
            if self.triggers[obj]['condition']():
                self.triggers[obj]['function']()

    def __str__(self):
        return '<Event: {}>'.format(self.__class__.__name__)

    def __repr__(self):
        return '<Event: {}>'.format(self.__class__.__name__)


class EndOfTurn(Event):
    pass
