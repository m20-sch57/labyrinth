# TODO: To put all consts here
# For everything.
reverse_direction = {'up': 'down', 'down': 'up',
                     'left': 'right', 'right': 'left',
                     'forward': 'backward', 'backward': 'forward',
                     'under': 'above', 'above': 'under'}
basic_directions = ['up', 'down', 'left', 'right']

# LabyrinthModule's consts.
INITIAL_STATES = {}

# Player's consts.
DEATH_MSG = '«Умирать — скучное и безотрадное дело. Мой вам совет — никогда этим не занимайтесь.»'

# Legs' consts.
UP_TURN = 'Идти вверх'
DOWN_TURN = 'Идти вниз'
RIGHT_TURN = 'Идти вправо'
LEFT_TURN = 'Идти влево'
WALL_MSG = 'Упсс. Стена'

# GlobalWall's consts.

# Wall's const.

# EmptyLocation's consts.
ENTER_MSG = 'Ты в пустой комнате'

# Hole's consts.
FALL_MSG = 'И в ямку бух!'
ENTER_HOLE_MSG = 'Ты в комнате с дырой'
TROUGH_HOLE_MSG = 'Вперёд, и только вперёд!'
INTO_TURN = 'В дыру'
TYPES_WHO_MUST_FALL_IN_IT = ['player', 'NPC']
AND_WHO_MUST_FALL_IN_IT = lambda obj: True
OR_WHO_MUST_FALL_IN_IT = lambda obj: False

# Gun's consts.
INITIAL_COUNT_OF_BULLETS = 3
CAN_PLAYER_HURT_HIMSELF = False
CAN_PLAYER_HURT_EVB_IN_SAME_LOC = True
FIRE_UP = 'Стрелять вверх'
FIRE_DOWN = 'Стрелять вниз'
FIRE_LEFT = 'Стрелять влево'
FIRE_RIGHT = 'Стрелять вправо'
FIRE_SUCCESS_MSG = 'Пиф-паф, ой-ой-ой. Снаряд попал в '
FIRE_FAILURE_MSG = 'Пиф-паф, ой-ой-ой. Снаряд ни в кого не попал.'

# Bomb's consts.
INITIAL_COUNT_OF_BOMBS = 3
BLOW_UP_UP = 'Подорвать сверху'
BLOW_UP_DOWN = 'Подорвать снизу'
BLOW_UP_LEFT = 'Подорвать слева'
BLOW_UP_RIGHT = 'Подорвать справа'
BLOW_UP_SUCCESS_MSG = 'Blowing shit up with homemade d-d-dynamite'
BLOW_UP_PROHIBITION_MSG = 'О, нет! Это же "ничего"! Увы, вы не можете сломать "ничего".'
BLOW_UP_FAILURE_MSG = 'Взорвать – взорвали, но толку-то?!'
BLOW_UP_NOT_PLAYERS_INJURING_MSG = 'О! Там были кто-то был, но не игроки'
BLOW_UP_SINGLE_INJURING_MSG = 'О! А там оказывается был(а) '
BLOW_UP_MASSIVE_INJURING_MSG = 'О! А там оказывается были '
CAN_PLAYER_HURT_EVB_IN_DIRECTION = True

# Arsenal's consts.

# FirstAidPost's consts.

# Bear's consts.
BEAR_MSG_ATTACK = 'Вас укусил медведь'

# Treasure's consts.
TAKE_TREASURE = 'Поднять клад'
DROP_TREASURE = 'Бросить клад'
CAN_PLAYER_DROP_TREASURE = True
WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED = False
SHOULD_HURT_PLAYER_DROP_TREASURE = True

# Exit's consts.
EXIT_GREETING_MSG = 'Ты вышел из Лабиринта. В этой комнате ты можешь передохнуть.'
EXIT_PRESENCE_MSGS = ['Как дела? Ты нашёл клад?',
                      'Как думаешь, почему медведи такие агрессивные?',
                      'Давай, быстрее! А то клад раньше тебя заберут!']
