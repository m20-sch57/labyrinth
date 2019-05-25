from database import Database
from flask import Flask, request
from flask_socketio import SocketIO
from flask_assets import Environment
from app.css_asset import css_asset

app = Flask(__name__)
app.config['SECRET_KEY'] = "qw75rs7fs5je5dd4s3sdf4s5liduf4dgg7fg6h5"
app.config['ASSETS_DEBUG'] = True
socketio = SocketIO(app)
assets = Environment(app)
assets.register('css_all', css_asset)
db = Database()

from app.room_namespace import init_room_namespaces
init_room_namespaces()

from app import routes
