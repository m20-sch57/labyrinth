from labyrinth_engine import load_lrmap, load_lrsave
from labyrinth_objects.Vanilla import Bear, Treasure

debug = True
if __name__ == '__main__':
    TestLR = load_lrmap('simple1', 'labyrinth_test_save', ['player #1'], 'imagepath')
    while not TestLR.is_game_ended:

        print('\n')
        ap = TestLR.get_active_player()

        print('┌──────────────────────────────────────────────────────────┐')
        if debug:
            print('│Player position    :  {:<36}│'.format(str(ap.get_parent())))
            print('│Creatures health   :  {:<36}│'.format(str(TestLR.get_unique('health').creature_hp)))
            #print('│Bear position      :  {:<36}│'.format(str(TestLR.get_objects(and_key=lambda x: isinstance(x, Bear))[0].get_parent())))
            print('│Treasure position  :  {:<36}│'.format(str(TestLR.get_objects(and_key=lambda x: isinstance(x, Treasure))[0].get_parent())))
            print('├──────────────────────────────────────────────────────────┤')
        print('│health             :  {:<36}│'.format(TestLR.get_unique('health').hp[ap]))
        print('│bombs              :  {:<36}│'.format(TestLR.get_unique('ammo').bombs[ap]))
        print('│bullets            :  {:<36}│'.format(TestLR.get_unique('ammo').bullets[ap]))
        print('└──────────────────────────────────────────────────────────┘')

        ats = TestLR.get_active_player_ats()
        ats[0:-1:4] = list(map(lambda x: '\n'+x, ats[0:-1:4]))
        print('; '.join(ats), end = '\n\n')

        msgs = TestLR.make_turn(input('(' + TestLR.get_active_player().get_username() + ') '))

        for player in msgs:
            print('\n'.join('[{}] - {}'.format(player, msg) for msg in msgs[player]))
