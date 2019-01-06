from Labyrinth.game import Labyrinth, Player
from Labyrinth.LS_walk import Legs, Wall, EmptyLocation
from Labyrinth.LS_hole import Hole

locations_list = [EmptyLocation() for _ in range(6)]
locations_list.append(Wall())
locations_list[1] = Hole()
locations_list[5] = Hole()
locations_list[1].set_fall_to(locations_list[5])
locations_list[5].set_fall_to(locations_list[1])
adjance_list = [{'up': 6, 'down': 3, 'right': 6, 'left': 6},
				{'up': 6, 'down': 4, 'right': 2, 'left': 6},
				{'up': 6, 'down': 5, 'right': 6, 'left': 1},
				{'up': 0, 'down': 6, 'right': 4, 'left': 6},
				{'up': 1, 'down': 6, 'right': 6, 'left': 3},
				{'up': 2, 'down': 6, 'right': 6, 'left': 6},
				{}]
items_list = [Legs()]
P = Player('player #1')
P.set_parent(locations_list[0])
players_list = [P]

# -------------
# | 0 | 1   2 |
# -           -
# | 3   4 | 5 |    HOLE  1<-->5
# -------------


MyLab = Labyrinth(locations_list, items_list, [], players_list, adjance_list)
while True:
	print()
	print(', '.join(MyLab.get_active_player_ats()))
	msgs = MyLab.make_turn(input())
	for player in msgs:
		print('[{}] - {}'.format(player, msgs[player]))
