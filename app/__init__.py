from flask import Flask, request
from database import Database
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "qw75rs7fs5je5dd4s3sdf4s5liduf4dgg7fg6h5"
socketio = SocketIO(app)
db = Database()

from app.room_namespace import init_room_namespaces
init_room_namespaces()

from app import routes
