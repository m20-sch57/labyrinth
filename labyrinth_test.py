from Labyrinth.game import Field, Labyrinth, Player, ObjectID
from Labyrinth.LS_move_and_bump import Legs, EmptyLocation, Outside, Wall
from Labyrinth.LS_appear_and_disappear import Hole
from Labyrinth.LS_hurt_and_break import Gun, Bomb, Arsenal, FirstAidPost
from Labyrinth.LS_NPCs import Bear
from Labyrinth.LS_silly_items import Treasure


def send_msg_func(msg, user_id):
    print('[{}] - {}'.format(user_id, msg))


# ------------------------------------------------
locations_list = [Outside()]
locations_list += [EmptyLocation() for _ in range(6)]
locations_list.append(Wall([
    (1, 'right'),
    (2, 'left')
                            ]))
locations_list.append(Wall([
    (5, 'right'),
    (6, 'left')
                            ]))
locations_list[2] = Hole(ObjectID('location', 6))
locations_list[6] = Hole(ObjectID('location', 2))
# -------------------------------------------------
adjacence_list = [{},
                  {'up': 0, 'down': 4, 'right': 7, 'left': 0},
                  {'up': 0, 'down': 5, 'right': 3, 'left': 7},
                  {'up': 0, 'down': 6, 'right': 0, 'left': 2},
                  {'up': 1, 'down': 0, 'right': 5, 'left': 0},
                  {'up': 2, 'down': 0, 'right': 8, 'left': 4},
                  {'up': 3, 'down': 0, 'right': 0, 'left': 8},
                  {},
                  {}]

# OutSide = 0
# ┌───┬───────┐
# │ 1 │ 2   3 │
# │           │
# │ 4   5 │ 6 │
# └───────┴───┘
# HOLES:  2↔6

# -------------------------------------------------
items_list = [Legs(), Gun(), Bomb()]
# -------------------------------------------------
P = Player('player #1')
Prey = Player('prey')
P.set_parent_id(ObjectID('location', 1))
Prey.set_parent_id(ObjectID('location', 4))
players_list = [P]
# -------------------------------------------------
NPCs_list = []


field = Field(adjacence_list, locations_list, items_list, players_list, NPCs_list)
MyLab = Labyrinth(field, send_msg_func)


MyLab.ready()
while True:
    print()
    print('Debug [player pos]', MyLab.get_active_player().get_parent_id().number,
          MyLab.get_active_player().get_parent_id().type)
    # print(field.locations_list[-1].behind_the_wall)
    print(', '.join(MyLab.get_active_player_ats()))
    MyLab.make_turn(input('(' + MyLab.get_active_player().get_user_id() + ') '))
