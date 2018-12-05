from Labyrinth.game import Field, Labyrinth, Player, ObjectID
from Labyrinth.LS_walk import Legs, Wall, EmptyLocation

def send_msg_func(msg, user_id):
	print('[{}] - {}'.format(user_id, msg))

locations_list = [EmptyLocation() for _ in range(6)]
locations_list.append(Wall())
adjance_list = [{'up':6, 'down':3, 'right':6, 'left':6},
				{'up':6, 'down':4, 'right':2, 'left':6},
				{'up':6, 'down':5, 'right':6, 'left':1},
				{'up':0, 'down':6, 'right':4, 'left':6},
				{'up':1, 'down':6, 'right':5, 'left':3},
				{'up':2, 'down':6, 'right':6, 'left':4},
				{}]
items_list = [Legs()]
P = Player('player #1')
P.set_parent_id(ObjectID('location', 0))
players_list = [P]

# ----------
# | 0 x 1 | 2 |
# ----------
# | 3 | 4 | 5 |
# ----------


field = Field(adjance_list, locations_list, items_list, players_list)
MyLab = Labyrinth(field, send_msg_func)

# print(MyLab.get_active_player_ats())
MyLab.ready()
while True:
	# print('Debug [player pos]', MyLab.get_active_player().get_parent_id().number, MyLab.get_active_player().get_parent_id().type)
	print()
	print(', '.join(MyLab.get_active_player_ats()))
	MyLab.make_turn(input())