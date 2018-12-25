from Labyrinth.LS_CONSTS import *

# LabyrinthObject is class of prototypes that can be used to make everything in Field.
class LabyrinthObject:

    # new available turn
    def new_at(self, function, condition_function, turn_name):

        # если turn_set не определён для предмета, то self.turn_set вызовет ошибку,
        # и тогда выполнится self.turn_set = {}
        try:
            self.turn_set
        except:
            self.turn_set = {}

        if turn_name not in self.turn_set:
            self.turn_set[turn_name] = {'function': function, 'condition': condition_function}

    # This two functions return object and parent's IDs.
    def get_object_id(self):
        return self.object_id

    def get_parent_id(self):
        return self.parent_id

    # This two function set object and parent's IDs to given value.
    def set_object_id(self, new_id):
        if type(new_id) is not ObjectID:
            raise ValueError('Invalid literal for set_object_id()')
        self.object_id = new_id

    def set_parent_id(self, new_id):
        if type(new_id) is not ObjectID:
            raise ValueError('Invalid literal for set_parent_id()')
        self.parent_id = new_id

    # Make false main-function in order not to remember every time to type it where it's not necessary.
    def main(self):
        pass


# Class for IDs. Nothing more.
class ObjectID:
    # Here object's type and number was declared in its ObjectID.
    # Every ID is type of object and its individual number among all objects with this type
    def __init__(self, object_type, object_number):
        self.type = object_type
        self.number = object_number
    # тип один из: location, item, player

    # This one helps to distinguish the differing and find the same objects.
    def __eq__(self, other):
        if type(other) is not ObjectID:
            raise ValueError('Invalid literal for __eq__')
        # Obviously it needs only to compare types and IDs
        return self.type == other.type and self.number == other.number


# Class of players of the game.
class Player(LabyrinthObject):
    # On the level of program player is LabyrinthObject.
    def __init__(self, user_id):
        self.user_id = user_id
        self.turn_set = {}  # На всякий случай
        self.states = {}

    def get_user_id(self):
        return self.user_id

    def hurt(self):
        if not self.states['hurt']:
            self.states['hurt'] = True
        else:
            ind = self.get_object_id().number
            self.set_object_id(ObjectID('dead_player', len(self.field.dead_players_list)))
            self.field.dead_players_list.append(self)
            del self.field.players_list[ind]
            for i in range(ind, len(self.field.players_list)):
                self.field.players_list[i].get_object_id().number = i
            del self.parent_id
            self.labyrinth.number_of_players -= 1
            self.labyrinth.send_msg(DEATH_MSG, self.user_id)


# Class of ALL field (including players and items). There is only one field in every game.
class Field:
    def __init__(self, adjacence_list, locations_list, items_list, players_list):
        # List of dicts of adjacences. It looks like [{'up': loc_above_id, 'down': under_id, 'left': left_id,
        # 'right': right_id}, ...]
        self.adjacence_list = adjacence_list
        self.locations_list = locations_list
        self.items_list = items_list
        # List of PLAYABLE players.
        self.players_list = players_list
        self.hurt_players = set()
        self.dead_players_list = []

        # раздаём всем id
        for i in range(len(self.locations_list)):
            self.locations_list[i].object_id = ObjectID('location', i)
        for i in range(len(self.items_list)):
            self.items_list[i].object_id = ObjectID('item', i)
        for i in range(len(self.players_list)):
            self.players_list[i].object_id = ObjectID('player', i)

    def get_neighbour_location(self, object_id, direction):
        if type(object_id) is not ObjectID or type(direction) is not str:
            raise ValueError('Invalid literal for get_neighbour_location()')
        return self.locations_list[self.adjacence_list[object_id.number][direction]]

    def get_neighbour_location_id(self, object_id, direction):
        if type(object_id) is not ObjectID or type(direction) is not str:
            raise ValueError('Invalid literal for get_neighbour_location()')
        return self.get_neighbour_location(object_id, direction).get_object_id()

    def get_object(self, object_id):
        if type(object_id) is not ObjectID:
            raise ValueError('Invalid literal for get_object()')
        lists = {
            'location': self.locations_list,
            'item': self.items_list,
            'player': self.players_list
        }
        return lists[object_id.type][object_id.number]

    def get_players_in_location(self, object_id):
        if type(object_id) is not ObjectID:
            raise ValueError('Invalid literal for get_players_in_location()')
        return list(filter(lambda player: player.get_parent_id() == object_id, self.players_list))

    def get_players_ids_in_location(self, object_id):
        if type(object_id) is not ObjectID:
            raise ValueError('Invalid literal for get_players_ids_in_location()')
        return list(map(lambda p: p.get_object_id(),
                        filter(lambda player: player.get_parent_id() == object_id, self.players_list)))


# Class of Labyrinths.
class Labyrinth:
    # Every Labyrinth is field and send_msg_function to send messages.
    def __init__(self, field, send_msg_function):
        self.send_msg = send_msg_function
        self.field = field

        self.active_player_number = 0
        self.number_of_players = len(self.field.players_list)

    def ready(self):
        # Создаёт всем локациям артибуты field и labyrinth и turn_set
        for location in self.field.locations_list:
            location.labyrinth = self
            location.field = self.field
            try:
                location.turn_set
            except:
                location.turn_set = {}
        for item in self.field.items_list:
            item.labyrinth = self
            item.field = self.field
            try:
                item.turn_set
            except:
                item.turn_set = {}

        for player in self.field.players_list:
            player.labyrinth = self
            player.field = self.field

            player.states['hurt'] = False
            player.states['count_of_bullets'] = INITIAL_COUNT_OF_BULLETS
            player.states['count_of_bombs'] = INITIAL_COUNT_OF_BOMBS

    def make_turn(self, turn):
        to_do = []

        # В списке возможных ходов, локаций и предметов ищем ход с именем turn
        # и запускаем действия найденных локаций и предметов.
        for location in self.field.locations_list:
            if turn in location.turn_set and location.turn_set[turn]['condition']():
                to_do.append(location.turn_set[turn]['function'])
        for item in self.field.items_list:
            if turn in item.turn_set and item.turn_set[turn]['condition']():
                to_do.append(item.turn_set[turn]['function'])
        # if not to_do:
        #     raise ValueError('Invalid turn')
        for function in to_do:
            function()

        # Запускаем для всех объектов main-функцию
        for location in self.field.locations_list:
            location.main()
        for item in self.field.items_list:
            item.main()

        # Делаем слудующего игрока активным
        self.active_player_number += 1
        self.active_player_number %= self.number_of_players

    def add_player(self, user_id):
        self.field.add_player(user_id, 0)
        self.number_of_players += 1

    def get_active_player(self):
        return self.field.players_list[self.active_player_number]

    def get_active_player_id(self):
        return self.get_active_player().get_object_id()

    def get_active_player_user_id(self):
        return self.get_active_player().user_id

    def get_next_active_player(self):
        return self.field.players_list[(self.active_player_number + 1) % len(self.field.players_list)]

    def get_next_active_player_id(self):
        return self.get_next_active_player().get_object_id()

    def get_active_player_ats(self):
        # Возвращает имена возможных ходов для активного игрока
        active_player_ats = []
        for location in self.field.locations_list:
            for turn in location.turn_set:
                if location.turn_set[turn]['condition']():
                    active_player_ats.append(turn)
        for item in self.field.items_list:
            for turn in item.turn_set:
                if item.turn_set[turn]['condition']():
                    active_player_ats.append(turn)
        return active_player_ats
