class Button:
    def __str__(self):
        return '<UI.button: {}: {}>'.format(self.btn_type, ', '.join(self.turns))

class CommonButton(Button):
    '''
    Обычная кнопка. 

    Активация равносильна
    выполнению команды, привязанной к кнопке

    turns - [<строковое представление хода>]

    image - путь до изображения, которое
    должно быть отображено на кнопке.
    '''
    def __init__(self, turns, image):
        self.btn_type = 'button'
        self.turns = turns
        self.image = image

    def get(self, ats):
        if self.turns in ats: 
            return {'type': self.btn_type,  'turns':self.turns, 'image': self.image}

class DirectionButton(Button):
    '''
    Кнопка с направлением

    Обычная кнопка, но с доп. возможность
    выбрать направление вверх, вниз, вправо
    или влево.

    turns - список из четырёх ходов.
    порядок: вверх, вниз, вправо, влево.
    '''
    def __init__(self, turns, image):
        self.btn_type = 'dbutton'
        self.turns = turns
        self.image = image

    def get(self, ats):
        if set(self.turns) & set(ats):
            return {'type': self.btn_type, 'turns': self.turns, 'image': self.image}

class ListButton(Button):
    '''
    Кнопка-список

    Позволяет объединить любое кол-во
    действий в одной кнопке.

    turn_images - список картинок для
    каждого хода, который можно сделать,
    использую эту кнопку.
    '''
    def __init__(self, turns, image, turn_images):
        self.btn_type = 'lbutton'
        self.turns = turns
        self.image = image
        self.turn_images = turn_images

    def get(self, ats):
        turns = []
        turn_images = []
        for i in range(len(self.turns)):
            if self.turns[i] in ats:
                turns.append(self.turns[i])
                turn_images.append(self.turn_images[i])
        if turns:
            return {'type': self.btn_type, 'turns': turns, 'image': self.image, 'turn_images': turn_images}