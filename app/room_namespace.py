from flask_socketio import Namespace, emit
from app import db, socketio

def init_room_namespaces():
    for room in db.rooms.page_by_page(1):
        if room:
            socketio.on_namespace(RoomNamespace('/' + room[0].id))

class RoomNamespace(Namespace):
    def on_connect(self):
        room_id = self.namespace[1:]
        if db.rooms.get(room_id):
            db.rooms.add_user(room_id)
            emit('update', {'event': 'player_enter_or_leave', 'players': ','.join(db.rooms.get(room_id).usernames)},
                  broadcast = True, namespace = self.namespace)

    def on_disconnect(self):
        room_id = self.namespace[1:]
        if db.rooms.get(room_id):
            db.rooms.remove_user(room_id)
            emit('update', {'event': 'player_enter_or_leave', 'players': ','.join(db.rooms.get(room_id).usernames)},
                  broadcast = True, namespace = self.namespace)
