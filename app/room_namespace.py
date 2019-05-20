from flask_socketio import Namespace, emit
from app import db, socketio
from app.help_functions import simple_render_template
from flask import session


def init_room_namespaces():
    for room in db.rooms.page_by_page(1):
        if room:
            socketio.on_namespace(RoomNamespace('/' + room[0].id))


class RoomNamespace(Namespace):
    def on_connect(self):
        room_id = self.namespace[1:]
        if db.rooms.get(room_id):
            db.rooms.add_user(room_id)
            emit('update', {'event': 'player_enter_or_leave', 'data':
                simple_render_template('rooms/_players_list.html', room=db.rooms.get(room_id))},
                 broadcast = True, namespace = self.namespace)

    def on_disconnect_request(self):
        room_id = self.namespace[1:]
        if db.rooms.get(room_id):
            db.rooms.remove_user(room_id)
            emit('update', {'event': 'player_enter_or_leave', 'data':
                simple_render_template('rooms/_players_list.html', room=db.rooms.get(room_id))},
                 broadcast = True, namespace = self.namespace)