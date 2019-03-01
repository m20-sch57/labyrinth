import sys
from LabyrinthEngine import Labyrinth, Player, load_lrmap, load_lrsave

sys.path.append('LabyrinthObjects')
from Vanilla import Legs, EmptyLocation, Outside, Wall, Hole, Gun, Bomb, Arsenal,\
    FirstAidPost, Bear, Treasure, Exit

#
# ┌───┬───────────┐
# │ 1 │ 2   3   4 │
# │               │
# │ 5   6 │ 7   8 │
# └───┐   ├───────┘
#     │ 9 │
#     └───┘
# OUTSIDE = 0
# HOLES:  2↔7
# ARSENAL: 4
# FIRST AID POST: 8
# EXIT: 9
#

debug = True
if __name__ == '__main__':
    TestLR = load_lrmap('example', 'example', ['player #1'])   
    print('All lrobjects: ', TestLR.get_objects())
    while True:
        print('\n')
        print('┌──────────────────────────────────────────────────────────┐')
        if debug:
            print('│Player position    :  {:<36}│'.format(str(TestLR.get_active_player().get_parent())))
            print('│Bear position      :  {:<36}│'.format(str(TestLR.get_objects(and_key = lambda x: isinstance(x, Bear))[0].get_parent())))
            print('│Treasure position  :  {:<36}│'.format(str(TestLR.get_objects(and_key = lambda x: isinstance(x, Treasure))[0].get_parent())))
            print('├──────────────────────────────────────────────────────────┤')
        print('\n'.join('│{:<19}:  {:<36}│'.format(str(k), str(v)) for k, v in TestLR.get_active_player().states.items()))
        print('└──────────────────────────────────────────────────────────┘')
        ats = TestLR.get_active_player_ats()
        ats[0:-1:4] = list(map(lambda x: '\n'+x, ats[0:-1:4]))
        print('; '.join(ats), end = '\n\n')
        msgs = TestLR.make_turn(input('(' + TestLR.get_active_player().get_username() + ') '))
        for player in msgs:
            print('\n'.join('[{}] - {}'.format(player, msg) for msg in msgs[player]))

