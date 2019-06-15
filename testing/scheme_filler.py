from os import chdir, getcwd, listdir

if 'labyrinth_maps' not in listdir('.'):
    chdir('\\'.join(getcwd().split('\\')[:-1]))

map_name = input()

with open('labyrinth_maps\\' + map_name + '\\map.scheme', 'w', encoding='utf-8') as scheme:
    scheme.write('\n')

    height, width = map(int, input().split())

    scheme.write(' ┌' + '─' * (4 * width - 1) + '┐\n')
    for i in range(height):
        scheme.write(' │')
        for j in range(width):
            s = str(i * width + j + 1)
            if len(s) < 3:
                s += ' '
            if len(s) < 3:
                s = ' ' + s
            if len(s) > 3:
                s = s[-3:]
            scheme.write(s)
            if j != width - 1:
                scheme.write(' ')
        scheme.write('│\n')
        if i != height - 1:
            scheme.write(' │' + ' ' * (4 * width - 1) + '│\n')
    scheme.write(' └' + '─' * (4 * width - 1) + '┘\n')

    scheme.write(' \n')
    scheme.write(' OUTSIDE = 0')