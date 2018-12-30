from flask import Flask
from database import Database
from labyrinths_list import LabyrinthsList

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"
dbase = Database()
labyrinths_list = LabyrinthsList()

from app import routes
