import sqlite3


class database: 
    def __init__(self):
        global cursor, conn
        #Создает объект базы данных. Рассчитано на запуск один раз, но проверяет наличие таблиц, чтобы не было ошибки SQL
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (login text PRIMARY KEY, pass_hash text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS maps (id integer PRIMARY KEY, maplink text, description text)''')
        conn.commit()
        
    def quit():
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
    
    #Я пока не понимаю, как работать с комнатами с помощью датабазы, поэтому их тут пока не будет
    
    def get_user(self, login):
        #Возвращает данные пользователя с данным логином
        cursor.execute('SELECT * FROM users WHERE login=?', [login])
        return cursor.fetchone()
    
    def get_map(self, mapid):
        cursor.execute('SELECT * FROM maps WHERE id=?', [mapid])
        return cursor.fetchone()

    
