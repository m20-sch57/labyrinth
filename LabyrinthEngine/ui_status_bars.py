class Bar:
    def __str__(self):
        return '<UI.bar: {}: {}>'.format(self.bar_type, self.name)


class StringBar(Bar):
    '''
    Текстовая строка состояния.
    Т.е значения предстовляется в текстовом виде

    values - словарь со значениями строки состояния
    для каждого игрока
    '''
    def __init__(self, name, init_values):
        self.bar_type = 'common'
        self.name = name
        self.values = init_values

    def set_value(self, new_value, player):
        self.values[player] = new_value

    def set_all_values(self, new_values):
        self.values = new_values

    def get(self, player):
        return {'type': self.bar_type, 'name': self.name, 'value': self.values[player]}
