from app import socketio, app
from database import Database

socketio.run(app, host = "0.0.0.0", port = 3000, debug = True)
