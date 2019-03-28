from flask_socketio import Namespace, emit
from app import db

class RoomNamespace(Namespace):
    def on_connect(self):
        room_id = self.namespace[1:]
        db.rooms.add_user(room_id)
        emit('update', {'event': 'player_enter_or_leave', 'players': ','.join(db.rooms.get(room_id).users)},
              broadcast = True, namespace = self.namespace)

    def on_disconnect(self):
        room_id = self.namespace[1:]
        db.rooms.remove_user(room_id)
        emit('update', {'event': 'player_enter_or_leave', 'players': ','.join(db.rooms.get(room_id).users)},
              broadcast = True, namespace = self.namespace)
