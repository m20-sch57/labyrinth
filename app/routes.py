from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', is_enter=False, is_index=True)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/profile')
def profile():
	pass

#бывшее /choose_your_room
@app.route('/room_list')
def room_list():
	pass

@app.route('/room/<room_id>')
def room():
	pass

@app.route('/rules')
def rules():
	return render_template('rules.html', is_enter=True)