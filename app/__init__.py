from flask import Flask
from database import Database
from flask_jsglue import JSGlue

app = Flask(__name__)
jsglue = JSGlue(app)
app.config['SECRET_KEY'] = "Your_secret_string"
dbase = Database()

from app import routes
