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
    def make_turn(self, turn):
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
        self.turns_log.append({'username': self.get_active_player_username(), 'turn': turn})

        # В списке возможных ходов локаций и предметов ищем ход с именем turn
        # и запускаем действия найденных локаций и предметов
        to_do = []
        for obj in self.get_all_objects():
            if turn in obj.get_turns() and obj.get_turns()[turn]['condition']():
                to_do.append(obj.get_turns()[turn]['function'])
        for function in to_do:
            function()

        # Запускаем для всех объектов main-функцию
        for obj in self.get_all_objects():
            obj.main()

        # Делаем следующего игрока активным
        while self.get_next_active_player_number() is None or self.is_game_ended:
            self.skip_turn()
        self.active_player_number = self.get_next_active_player_number()

        # Уменьшаем у всех игроков пропуски ходов.
        for player in self.players_list:
            if player.have_flag('skip_turns'):
                count = player.get_flag('skip_turns')
                if count > 1:
                    player.set_flag('skip_turns', count - 1)
                elif count == 1:
                    player.delete_flag('skip_turns')

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
        for obj in self.get_all_objects():
            obj.main()

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
                return list(filter(lambda turn: turn['player'] in username, self.turns))
            else:
                return list(filter(lambda turn: turn['player'] in username, self.turns))[-number]

    def end_game(self):
        self.is_game_ended = True

    # Активный игрок.
    def get_next_active_player_number(self):
        apn = self.active_player_number
        for i in range(len(self.players_list)):
            apn += 1
            apn %= len(self.players_list)
            if not self.players_list[apn].have_flag('skip_turns'):
                return apn
        return None

    def get_next_active_player(self):
        apn = self.get_next_active_player_number()
        return self.players_list[apn] if apn is not None else None

    def get_active_player(self):
        return self.players_list[self.active_player_number]

    def get_active_player_username(self):
        return self.get_active_player().get_username()

    def get_active_player_ats(self):
        """
        Возвращает возможные для активного игрока ходы
        """

        active_player_ats = []
        for obj in self.get_all_objects():
            for turn in obj.get_turns():
                if obj.get_turns()[turn]['condition']():
                    active_player_ats.append(turn)

        return active_player_ats

    # Объекты Лабиринта.
    def get_all_objects(self):
        return self.locations | self.items | self.creatures | set(self.players_list)

    def get_objects(self, lrtype=['location', 'item', 'player', 'creature'],
                    and_key=lambda x: True, or_key=lambda x: False):
        return list(filter(lambda obj: obj.lrtype in lrtype and and_key(obj) or or_key(obj), self.get_all_objects()))

    def save(self):
        save = {
        'seed': self.seed,
        'loadseed': self.loadseed,
        'users': list(map(lambda user: user.get_username(), self.players_list)),
        'turns': self.turns_log,
        }
        return json.dumps(save, indent=4, ensure_ascii=False)

    def get_buttons(self):
        ats = self.get_active_player_ats()
        buttons = []
        for obj in self.get_all_objects():
            for btn in obj.get_buttons():
                btn_info = btn.get(ats, self.imagepath)
                if btn_info is not None:
                    buttons.append(btn_info)
        return buttons

    def get_bars(self, username):
        bars = []
        player = self.get_objects('player', lambda p: p.username == username)[0]
        for obj in self.get_all_objects():
            for bar in obj.get_bars():
                bar_info = bar.get(player)
                bars.append(bar_info)
        return bars
