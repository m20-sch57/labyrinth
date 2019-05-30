from database import Database, drop_db
import os

drop_db()
db = Database()

db.users.add('yandex', 'password')
db.users.add('firefox', 'password')
db.users.add('edge', 'password')
db.users.add('gtivansan', 'password')
db.users.add('username', 'password')
db.users.add('lounres', 'password')
db.users.add('root', 'password')
db.users.add('admin', 'password')

for foldername in os.listdir('labyrinth_maps'):
    db.maps.add(foldername, 'root', 
                open('labyrinth_maps/'+foldername+'/descr.txt', 'r', encoding='utf-8').read(),
                open('labyrinth_maps/'+foldername+'/map.json',  'r', encoding='utf-8').read())