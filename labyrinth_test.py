from Labyrinth.itemLO_legs import Legs
from Labyrinth.locLO_empty import EmptyLocation
from Labyrinth.locLO_hole import HoleLocation
from Labyrinth.locLO_global_wall import GlobalWall
from Labyrinth.game import ObjectID, Field, Labyrinth

def send_msg_func(msg, user_id):
	print('[{}] - {}'.format(user_id, msg))

field = Field()
MyLab = Labyrinth(field, send_msg_func)

field.add_location(GlobalWall(), [0, 0, 0, 0])
field.add_location(EmptyLocation(), [0, 4, 2, 0])
field.add_location(EmptyLocation(), [0, 5, 3, 1])
field.add_location(HoleLocation(6), [0, 6, 0, 2])
field.add_location(EmptyLocation(), [1, 0, 5, 0])
field.add_location(EmptyLocation(), [2, 0, 6, 4])
field.add_location(HoleLocation(3), [1, 0, 1, 1])

field.add_player(0, 1)

L = Legs()
field.add_item(L, 0, parent_type='location')

# print(MyLab.get_active_player_ats())
MyLab.ready()
while True:
	print(MyLab.get_active_player().get_parent_id().nomber, MyLab.get_active_player().get_parent_id().type)
	print(MyLab.get_active_player_ats())
	MyLab.make_turn(input())