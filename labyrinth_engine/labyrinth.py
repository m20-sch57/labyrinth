from labyrinth_engine.event import MainEvent, EndOfTurn
import random
import json
import sys


class Labyrinth:
    def __init__(self, locations, items, creatures, players, adjacence_list, settings, imagepath='',
                 seed=random.randrange(sys.maxsize), loadseed=random.randrange(sys.maxsize)):

        random.seed(seed)
        self.seed = seed
        self.loadseed = loadseed
        self.imagepath = imagepath

        self.unique_objects = {}

        self.end_of_turn_event = EndOfTurn()
        self.main_event = MainEvent()

        for i in range(len(locations)):
            locations[i].directions = {
                direction: locations[k] for direction, k in adjacence_list[i].items()}
        for player in players:
            player.labyrinth = self
            for flag in settings['player'].get('flags', []):
                player.set_flag(flag)

        lrtypes = {
            'location': locations,
            'item': items,
            'creature': creatures}         
        lrlist = locations, items, creatures, players

        for lrtype in lrtypes:
            for i in range(len(lrtypes[lrtype])):
                obj = lrtypes[lrtype][i]
                obj.labyrinth = self
                for flag in settings[obj.lrtype + 's'][i].get('flags', []):
                    obj.set_flag(flag)
                obj.set_name(settings[obj.lrtype + 's'][i].get('name', ''))
                obj.set_settings(settings[obj.lrtype + 's'][i], *lrlist)

        self.locations = set(locations)
        self.items = set(items)
        self.creatures = set(creatures)
        self.players_list = players

        self.to_send = {}
        self.active_player_number = 0
        self.is_game_ended = False

        """
        turns_log
        [{'player': first_player_name, 'turn': his_turn}, {'player': second_player_name, 'turn': his_turn}, ...]
        msgs_log
        {player_name: [first_msg, second_msg, ...]}
        """
        self.turns_log = []
        self.msgs_log = {}

        # Пилим настройки.
        with open('labyrinth_engine\\default_settings.json', 'r', encoding='utf-8') as def_set_file:
            default_settings = json.load(def_set_file).get('Labyrinth', {})
            default_settings.update(settings['Labyrinth'])
            settings['Labyrinth'] = default_settings

        self.MAX_COUNT_OF_SKIPS = settings['Labyrinth']['max_count_of_skips']

    # Сообщения.
    def send_msg(self, msg, player, priority=0):
        clear_list = {player.get_username(): [] for player in self.players_list}
        if priority not in self.to_send:
            self.to_send[priority] = clear_list
        self.to_send[priority][player.get_username()].append(msg)

    def clear_to_send(self):
        self.to_send = {}

    def regularize_to_send(self):
        answer = {player.get_username(): [] for player in self.players_list}
        for key in sorted(self.to_send, reverse=True):
            for player, msg_list in self.to_send[key].items():
                answer[player] += msg_list

        return answer

    def player_to_send(self, username):
        return self.regularize_to_send()[username]

    def get_msgs(self, username):
        """
        Возвращает все сообщения отосланные игроку username
        """

        if username in self.msgs_log:
            return self.msgs_log[username]
        else:
            return []

    # Уникальные предметы.
    def set_unique(self, obj, key):
        if key in self.unique_objects:
            pass
            # тут должен быть какой-то идейный warning
        else:
            self.unique_objects[key] = obj

    def get_unique(self, key):
        return self.unique_objects[key]

    # Ход игрока.
    def make_turn(self, event):
        """
        Вызвать эту функцию, если активный игрок сделал ход turn

        to_send: словарь сообщения для отправки.
        {username1: msg1, ... , username_n: msg_n}
        """

        # обнуляем to_send
        self.clear_to_send()

        if self.is_game_ended:
            return self.regularize_to_send()

        # обновляем лог ходов
        self.turns_log.append({'username': self.get_active_player_username(), 'turn': event.name})

        # Запускаем событие.
        event.trigger()

        # Запускаем для всех объектов main-функцию
        self.main_event.trigger()

        # Уменьшаем у всех игроков пропуски ходов.
        for player in self.players_list:
            if player.have_flag('skip_turns'):
                count = player.get_flag('skip_turns')
                if count > 1:
                    player.set_flag('skip_turns', count - 1)
                elif count == 1:
                    player.delete_flag('skip_turns')

        # Делаем следующего игрока активным
        count_of_skips = 0
        while self.get_next_active_player_number() is None and not self.is_game_ended:
            if count_of_skips > self.MAX_COUNT_OF_SKIPS >= 0:
                self.end_game()
            self.skip_turn()
            count_of_skips += 1
        self.active_player_number = self.get_next_active_player_number()

        # Запускаем end-of-turn-функцию
        self.end_of_turn_event.trigger()

        # Обновляем лог сообщений
        for player in self.players_list:
            username = player.get_username()
            if username in self.msgs_log:
                self.msgs_log[username].append(self.player_to_send(username))
            else:
                self.msgs_log[username] = [self.player_to_send(username)]

        # возвращаем все сообщения, которые нужно отправить
        return self.regularize_to_send()

    def skip_turn(self):
        # Запускаем для всех объектов main-функцию
        self.main_event.trigger()

        # Уменьшаем у всех игроков пропуски ходов.
        for player in self.players_list:
            if player.have_flag('skip_turns'):
                count = player.get_flag('skip_turns')
                if count > 1:
                    player.set_flag('skip_turns', count - 1)
                elif count == 1 or count == 0:
                    player.delete_flag('skip_turns')

    def get_turns(self, number=None, username=None):
        """
        Возвращает все ходы сделанные игроками
        Возвращает ходы сделанные только указанным игроками, если указан параметр username
        Возвращает ход под номером number с конца, если указан параметр number
        Например get_turns(1, 'Вася') вернёт последний ход Васи
        """

        if username is None:
            if number is None:
                return self.turns_log
            else:
                return self.turns_log[-number]
        else:
            if number is None:
                return list(filter(lambda turn: turn['player'] in username, self.turns_log))
            else:
                return list(filter(lambda turn: turn['player'] in username, self.turns_log))[-number]

    def end_game(self):
        self.is_game_ended = True

    # Активный игрок.
    def get_next_active_player_number(self):
        apn = self.active_player_number
        for i in range(len(self.players_list)):
            apn = (apn + 1) % len(self.players_list)
            if not self.players_list[apn].have_flag('skip_turns'):
                return apn
        return None

    def get_next_active_player(self):
        apn = self.get_next_active_player_number()
        return self.players_list[apn] if apn is not None else None

    def get_active_player(self):
        return self.players_list[self.active_player_number]

    def get_active_player_username(self):
        return self.get_active_player().get_username() if self.get_active_player() is not None else None

    def get_active_player_ats(self):
        """
        Возвращает возможные для активного игрока ходы
        """

        active_player_ats = []
        for button in self.get_buttons():
            active_player_ats += [{'name': button.names[i], 'button': button, 'index': i} for i in range(len(button.names))]

        return active_player_ats

    # Объекты Лабиринта.
    def get_all_objects(self):
        return self.locations | self.items | self.creatures | set(self.players_list)

    def get_objects(self, lrtype=['location', 'item', 'player', 'creature'], class_names=[], flags=[], key=lambda x: True):
        return list(filter(lambda obj:
                           obj.lrtype in lrtype and
                           (type(obj).__name__ in class_names or not class_names) and
                           (all(obj.have_flag(flag) for flag in flags) or not flags) and
                           key(obj),
                           self.get_all_objects()))

    def save(self):
        save = {
        'seed': self.seed,
        'loadseed': self.loadseed,
        'users': list(map(lambda user: user.get_username(), self.players_list)),
        'turns': self.turns_log,
        }
        return json.dumps(save, indent=4, ensure_ascii=False)

    def get_buttons(self):
        buttons = []
        for obj in self.get_all_objects():
            buttons += obj.get_buttons()
        return buttons

    def get_bars(self):
        bars = []
        for obj in self.get_all_objects():
            bars += obj.get_bars()
        return bars
