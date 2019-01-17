from LabyrinthEngine import Labyrinth, Player
from LabyrinthObjects import Legs, EmptyLocation, Outside, Wall, Hole, Gun, Bomb, Arsenal,\
    FirstAidPost, Bear, Treasure, Exit


# ------------------------------------------------
locations_list = [Outside()]
locations_list += [EmptyLocation() for _ in range(9)]
locations_list[2] = Hole()
locations_list[7] = Hole()
locations_list[2].set_fall_to(locations_list[7])
locations_list[7].set_fall_to(locations_list[2])
locations_list[4] = Arsenal()
locations_list[8] = FirstAidPost()
locations_list[9] = Exit()
locations_list.append(Wall([
    (locations_list[1], 'right'),
    (locations_list[2], 'left')
                            ]))
locations_list.append(Wall([
    (locations_list[6], 'right'),
    (locations_list[7], 'left')
                            ]))

for i in range(len(locations_list)):
    locations_list[i].name = i
# -------------------------------------------------
adjacence_list = [{},
                  {'up': 0, 'down': 5, 'right': 10, 'left': 0},
                  {'up': 0, 'down': 6, 'right': 3, 'left': 10},
                  {'up': 0, 'down': 7, 'right': 4, 'left': 2},
                  {'up': 0, 'down': 8, 'right': 0, 'left': 3},
                  {'up': 1, 'down': 0, 'right': 6, 'left': 0},
                  {'up': 2, 'down': 9, 'right': 11, 'left': 5},
                  {'up': 3, 'down': 0, 'right': 8, 'left': 11},
                  {'up': 4, 'down': 0, 'right': 0, 'left': 7},
                  {'up': 6, 'down': 0, 'right': 0, 'left': 0},
                  {},
                  {}]

# OutSide = 0
# ┌───┬───────────┐
# │ 1 │ 2   3   4 │
# │               │
# │ 5   6 │ 7   8 │
# └───┐   ├───────┘
#     │ 9 │
#     └───┘
# HOLES:  2↔7
# ARSENAL: 4
# FIRST AID POST: 8
# EXIT: 9

# -------------------------------------------------
tres = Treasure(True)
tres.set_parent(locations_list[3])
items_list = [Legs(), Gun(), Bomb(), tres]
# -------------------------------------------------
player = Player('player #1')
prey = Player('prey')
player.set_parent(locations_list[1])
prey.set_parent(locations_list[5])
players_list = [player]
# -------------------------------------------------
bear = Bear()
bear.set_parent(locations_list[4])
NPCs_list = []


MyLab = Labyrinth(locations_list, items_list, NPCs_list, players_list, adjacence_list)


while True:
    print()
    print('Debug [player pos]', MyLab.get_active_player().get_parent())
    # print(MyLab.locations)
    print('Debug [bear pos]', bear.get_parent())
    print(MyLab.get_active_player().states)
    print(', '.join(MyLab.get_active_player_ats()))
    msgs = MyLab.make_turn(input('({}) '.format(MyLab.get_active_player().get_username())))
    for player in msgs:
        for msg in msgs[player]:
            print('[{}] - {}'.format(player, msg))
