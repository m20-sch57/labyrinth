from os import chdir, getcwd, listdir

if 'labyrinth_maps' not in listdir('.'):
    chdir('\\'.join(getcwd().split('\\')[:-1]))

map_name = input()

with open('labyrinth_maps\\' + map_name + '\\map.json', 'w', encoding='utf-8') as Map:
    Map.write('{\n')

    height, width = map(int, input().split())
    all = height * width

    Map.write('    "locations":\n')
    Map.write('    [\n')
    Map.write('        {\n')
    Map.write('            "module": "labyrinth_objects.Vanilla",\n')
    Map.write('            "class_name": "Outside"\n')
    Map.write('        }\n')
    if all != 0:
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
    Map.write('    ],\n')
    Map.write('    "creatures":\n')
    Map.write('    [\n')
    Map.write('    ],\n')
    Map.write('    "adjacence_list":\n')
    Map.write('    [\n')
    Map.write('        {}\n')
    if all != 0:
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
    Map.write('        "locations":\n')
    Map.write('        [\n')
    Map.write('            {\n')
    Map.write('                "name": "Out"\n')
    Map.write('            }\n')
    if all != 0:
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
    Map.write('                "from": [3, 17]\n')
    Map.write('            }\n')
    Map.write('        }\n')
    Map.write('    }\n')
    Map.write('}\n')
