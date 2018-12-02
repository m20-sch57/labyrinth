from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "Your_secret_string"

from app import routes