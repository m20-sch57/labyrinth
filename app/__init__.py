from flask import Flask
from database import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"
dbase = Database()

from app import routes
