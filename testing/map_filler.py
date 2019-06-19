from os import chdir, getcwd, listdir

if 'labyrinth_maps' not in listdir('.'):
    chdir('\\'.join(getcwd().split('\\')[:-1]))

map_name = input('Map name?\n')

with open('labyrinth_maps\\' + map_name + '\\map.json', 'w', encoding='utf-8') as Map:
    Map.write('{\n')

    height, width = map(int, input('Height and width?\n').split())
    All = height * width

    Map.write('    "locations":\n')
    Map.write('    [\n')
    Map.write('        {\n')
    Map.write('            "module": "labyrinth_objects.Vanilla",\n')
    Map.write('            "class_name": "Outside"\n')
    Map.write('        }\n')
    if All != 0:
        Map.write('    ,\n')

    for i in range(height):
        for j in range(width):
            Map.write('        {\n')
            Map.write('            "module": "labyrinth_objects.Vanilla",\n')
            Map.write('            "class_name": "EmptyLocation"\n')
            Map.write('        }' + ',' * int(j != width - 1) + '\n')

        if i != height - 1:
            Map.write('    ,\n')

    Map.write('    ],\n')
    Map.write('    "items":\n')
    Map.write('    [\n')

    decision = {'Legs': False,
                'Gun': False,
                'Bomb': False,
                'Health': False,
                'Ammo': False,
                'Treasure': False,
                'ExitChecker': False,
                'Death': False}

    s = ''
    while s not in ['yes', 'no']:
        s = input('Legs? (yes/no)\n')
    if s == 'yes':
        Map.write('        {\n')
        Map.write('            "module":"labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name":"Legs"\n')
        Map.write('        }')
        decision['Legs'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('Gun? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "Gun"\n')
        Map.write('        }')
        decision['Gun'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('Bomb? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "Bomb"\n')
        Map.write('        }')
        decision['Bomb'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('Health? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "Health"\n')
        Map.write('        }')
        decision['Health'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('Ammo? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "Ammo"\n')
        Map.write('        }')
        decision['Ammo'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('Treasure? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "Treasure"\n')
        Map.write('        }')
        decision['Treasure'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('ExitChecker? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "ExitChecker"')
        Map.write('        }')
        decision['ExitChecker'] = True

    s = ''
    while s not in ['yes', 'no']:
        s = input('Death? (yes/no)\n')
    if s == 'yes':
        if any(decision.values()):
            Map.write(',\n')
        Map.write('        {\n')
        Map.write('            "module": "labyrinth_objects.Vanilla",\n')
        Map.write('            "class_name": "Death"')
        Map.write('        }')
        decision['Death'] = True

    if any(decision.values()):
        Map.write('\n')

    Map.write('    ],\n')
    Map.write('    "creatures":\n')
    Map.write('    [\n')
    Map.write('    ],\n')
    Map.write('    "adjacence_list":\n')
    Map.write('    [\n')
    Map.write('        {}\n')
    if All != 0:
        Map.write('    ,\n')

    for i in range(height):
        for j in range(width):
            Map.write('        {\n')
            Map.write('            "up": ' + str(0 if i == 0 else (i - 1) * width + j + 1) + ',\n')
            Map.write('            "down": ' + str(0 if i == height - 1 else (i + 1) * width + j + 1) + ',\n')
            Map.write('            "left": ' + str(0 if j == 0 else i * width + j) + ',\n')
            Map.write('            "right": ' + str(0 if j == width - 1 else i * width + j + 2) + '\n')
            Map.write('        }' + ',' * int(j != width - 1) + '\n')

        if i != height - 1:
            Map.write('    ,\n')

    Map.write('    ],\n')
    Map.write('    "settings":\n')
    Map.write('    {\n')
    Map.write('        "Labyrinth":\n')
    Map.write('        {\n')
    Map.write('        \n')
    Map.write('        },\n')
    Map.write('        "locations":\n')
    Map.write('        [\n')
    Map.write('            {\n')
    Map.write('                "name": "Out"\n')
    Map.write('            }\n')
    if All != 0:
        Map.write('        ,\n')

    for i in range(height):
        for j in range(width):
            Map.write('            {\n')
            Map.write('                "name": "' + str(i * width + j + 1) + '"\n')
            Map.write('            }' + ',' * int(j != width - 1) + '\n')

        if i != height - 1:
            Map.write('        ,\n')

    Map.write('        ],\n')
    Map.write('        "items":\n')
    Map.write('        [\n')

    is_first = True
    if decision['Legs']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Legs"\n')
        Map.write('            }')

    if decision['Gun']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Gun"\n')
        Map.write('            }')

    if decision['Bomb']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Bomb"\n')
        Map.write('            }')

    if decision['Health']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Health"\n')
        Map.write('            }')

    if decision['Ammo']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Ammo"\n')
        Map.write('            }')

    if decision['Treasure']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Treasure",\n')
        Map.write('                "is_true": true,\n')
        pos = ''
        while True:
            try:
                pos = int(pos)
                if 0 < pos < All:
                    break
            except:
                pos = input("Treasure's position?\n")
        Map.write('                "position":' + str(pos) + '\n')
        Map.write('            }')

    if decision['ExitChecker']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "ExitChecker"\n')
        Map.write('            }')

    if decision['Death']:
        if not is_first:
            Map.write(',\n')
        else:
            is_first = False
        Map.write('            {\n')
        Map.write('                "name": "Death\n')
        Map.write('            }')

    if any(decision.values()):
        Map.write('\n')

    Map.write('        ],\n')
    Map.write('        "creatures":\n')
    Map.write('        [\n')
    Map.write('        ],\n')
    Map.write('        "player":\n')
    Map.write('        {\n')
    Map.write('            "flags": ["drop_items_when_injured"],\n')
    Map.write('            "start_positions":\n')
    Map.write('            {\n')
    Map.write('                "distribution": "random",\n')
    Map.write('                "from": []\n')
    Map.write('            }\n')
    Map.write('        }\n')
    Map.write('    }\n')
    Map.write('}\n')
