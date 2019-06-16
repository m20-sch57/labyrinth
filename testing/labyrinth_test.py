from labyrinth_engine import load_map, load_save
from labyrinth_objects.Vanilla import Bear, Treasure
import json
from os import chdir, getcwd, listdir

if 'labyrinth_maps' not in listdir('.'):
    chdir('\\'.join(getcwd().split('\\')[:-1]))

debug = True
if __name__ == '__main__':
    # save = '''{
    # "seed": 1278969433893649490,
    # "turns": [
    #     {
    #         "username": "player #1",
    #         "turn": "Идти вверх"
    #     },
    #     {
    #         "username": "player #2",
    #         "turn": "Подорвать справа"
    #     }
    # ],
    # "users": [
    #     "player #1",
    #     "player #2"
    # ],
    # "loadseed": 8316663732998351558
    # }'''

    with open('labyrinth_maps/test(small)/map.json', 'r', encoding='utf-8') as f:
        _map = f.read()

    # TestLR = load_save(save, _map)
    TestLR = load_map(_map, ['player #1'])
    while not TestLR.is_game_ended:

        print('\n')
        ap = TestLR.get_active_player()

        print('┌──────────────────────────────────────────────────────────┐')
        if debug:
            print('│Player position    :  {:<36}│'.format(str(ap.get_parent())))
            try:
                print('│Creatures health   :  {:<36}│'.format(str(TestLR.get_unique('health').creature_hp)))
            except:
                pass
            for bear in TestLR.get_objects(class_names=['Bear']):
                print('│Bear position      :  {:<36}│'.format(str(bear.get_parent())))
            for treasure in TestLR.get_objects(class_names=['Treasure']):
                print('│Treasure position  :  {:<36}│'.format(str(treasure.get_parent())))
            print('├──────────────────────────────────────────────────────────┤')
        try:
            print('│health             :  {:<36}│'.format(TestLR.get_unique('health').hp[ap]))
        except:
            pass
        try:
            print('│bombs              :  {:<36}│'.format(TestLR.get_unique('ammo').bombs[ap]))
        except:
            pass
        try:
            print('│bullets            :  {:<36}│'.format(TestLR.get_unique('ammo').bullets[ap]))
        except:
            pass
        print('└──────────────────────────────────────────────────────────┘')

        ats = TestLR.get_active_player_ats()
        ats[0:-1:4] = list(map(lambda x: '\n'+x, ats[0:-1:4]))
        print('; '.join(ats), end='\n\n')

        msgs = TestLR.make_turn(input('(' + TestLR.get_active_player().get_username() + ') '))
        #print(TestLR.save())

        for player in msgs:
            print('\n'.join('[{}] - {}'.format(player, msg) for msg in msgs[player]))
