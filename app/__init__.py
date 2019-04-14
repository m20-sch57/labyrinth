from flask import Flask, request
from database import Database
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"
socketio = SocketIO(app)
db = Database()

from app.room_namespace import init_room_namespaces
init_room_namespaces()

from app import routes

socketio.run(app, host="0.0.0.0", port=3000, debug=True)
