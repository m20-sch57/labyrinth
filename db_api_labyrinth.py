import sqlite3


class database: 
    def __init__(self):
        #Создает объект базы данных. Рассчитано на запуск один раз, но проверяет наличие таблиц, чтобы не было ошибки SQL
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (login text PRIMARY KEY, pass_hash text)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS maps (id integer PRIMARY KEY, maplink text, description text)''') #description - это описание карты, дающееся создателем
        self.cursor.execute('CREATE TABLE IF NOT EXISTS rooms (id integer PRIMARY KEY, joinlink text, settings text, description text, players text)') #settings - настройки комнаты, как именно хранятся - пока непонятно, тип text, ибо самый универсальный
        self.conn.commit()
        
    def quit(self):
        self.conn.close()
        
    def add_user(self, login, pass_hash):
        #Добавляет пользователя в базу по логину и паролю. Хеширование должна делать другая функция(!)
        user_data = [login, pass_hash]
        self.cursor.execute('INSERT INTO users VALUES (?, ?)', user_data)
        self.conn.commit()
        
    def add_map(self, maplink, description):
        map_data = [maplink, description]
        self.cursor.execute('INSERT INTO maps VALUES (NULL, ?, ?)', map_data)
        self.conn.commit()
    
    def add_room(self, joinlink, settings, description, creator):
        room_data = [joinlink, settings, description, creator]
        self.cursor.execute('INSERT INTO rooms VALUES (NULL, ?, ?, ?, ?)', room_data)
        self.conn.commit()
    
    def get_user(self, login):
        #Возвращает данные пользователя с данным логином
        self.cursor.execute('SELECT * FROM users WHERE login=?', [login])
        return self.cursor.fetchone()
    
    def get_map(self, mapid):
        self.cursor.execute('SELECT * FROM maps WHERE id=?', [mapid])
        return self.cursor.fetchone()
    
    def get_room(self, roomid):
        self.cursor.execute('SELECT * FROM rooms WHERE id=?', [roomid])
        return self.cursor.fetchone()
    
    def add_player(self, roomid, player):
        data = get_room(self, roomid)
        self.cursor.execute('DELETE * FROM rooms WHERE id=?', [roomid])
        data[-1] = data[-1] + ' ' + player
        self.cursor.execute('INSERT INTO rooms VALUES (?, ?, ?, ?, ?)', data)
        self.conn.commit()
        
