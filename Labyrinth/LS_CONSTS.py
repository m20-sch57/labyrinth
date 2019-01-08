# TODO: To put all consts here
# For everything.
reverse_direction = {'up': 'down', 'down': 'up',
                     'left': 'right', 'right': 'left',
                     'forward': 'backward', 'backward': 'forward',
                     'under': 'above', 'above': 'under'}
basic_directions = ['up', 'down', 'left', 'right']

# Labyrinth's consts.
INITIAL_STATES = {}

# Player's consts.
DEATH_MSG = '«Умирать — скучное и безотрадное дело. Мой вам совет — никогда этим не занимайтесь.»'

# Legs' consts.
UP_TURN = 'Идти вверх'
DOWN_TURN = 'Идти вниз'
RIGHT_TURN = 'Идти вправо'
LEFT_TURN = 'Идти влево'
WALL_MSG = 'Упсс. Стена'

# Wall's const.

# EmptyLocation's consts.
ENTER_MSG = 'Ты в пустой комнате'

# Hole's consts.
FALL_MSG = 'И в ямку бух!'
ENTER_HOLE_MSG = 'Ты в комнате с дырой'
TROUGH_HOLE_MSG = 'Вперёд, и только вперёд!'
INTO_TURN = 'В дыру'

# Bullet's consts.
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
BLOW_UP_SINGLE_INJURING_MSG = 'О! А там оказывается были '
BLOW_UP_MASSIVE_INJURING_MSG = 'О! А там оказывается был '
CAN_PLAYER_HURT_EVB_IN_DIRECTION = True

# Treasure's consts.
TAKE_TREASURE = 'Поднять клад'
DROP_TREASURE = 'Бросить клад'
CAN_PLAYER_DROP_TREASURE = True
WILL_TREASURE_RETURNS_BACK_WHEN_IS_DROPPED = False
SHOULD_HURT_PLAYER_DROP_TREASURE = True
