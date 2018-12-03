import sqlite3


class database: 
    def __init__(self):
        #Создает объект базы данных. Рассчитано на запуск один раз, но проверяет наличие таблиц, чтобы не было ошибки SQL
        self.conn = sqlite3.connect('database.db')
        self.cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (login text PRIMARY KEY, pass_hash text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS maps (id integer PRIMARY KEY, maplink text, description text)''') #description - это описание карты, дающееся создателем
        cursor.execute('CREATE TABLE IF NOT EXISTS rooms (id integer PRIMARY KEY, joinlink text, settings text, description text, players text)') #settings - настройки комнаты, как именно хранятся - пока непонятно, тип text, ибо самый универсальный
        conn.commit()
        
    def quit(self):
        conn.close()
        
    def add_user(self, login, pass_hash):
        #Добавляет пользователя в базу по логину и паролю. Хеширование должна делать другая функция(!)
        user_data = [login, pass_hash]
        cursor.execute('INSERT INTO users VALUES (?, ?)', user_data)
        conn.commit()
        
    def add_map(self, maplink, description):
        map_data = [maplink, description]
        cursor.execute('INSERT INTO maps VALUES (NULL, ?, ?)', map_data)
        conn.commit()
    
    def add_room(self, joinlink, settings, description, creator):
        room_data = [joinlink, settings, description, creator]
        cursor.execute('INSERT INTO rooms VALUES (NULL, ?, ?, ?, ?)', room_data)
        conn.commit()
    
    def get_user(self, login):
        #Возвращает данные пользователя с данным логином
        cursor.execute('SELECT * FROM users WHERE login=?', [login])
        return cursor.fetchone()
    
    def get_map(self, mapid):
        cursor.execute('SELECT * FROM maps WHERE id=?', [mapid])
        return cursor.fetchone()
    
    def get_room(self, roomid):
        cursor.execute('SELECT * FROM rooms WHERE id=?', [roomid])
        return cursor.fetchone()
    
    def add_player(self, roomid, player):
        data = get_room(self, roomid)
        cursor.execute('DELETE * FROM rooms WHERE id=?', [roomid])
        data[-1] = data[-1] + ' ' + player
        cursor.execute('INSERT INTO rooms VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
    