from app import app
from flask import render_template, request, session, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', username = session.get('username'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		print('test')
		session['username'] = request.form.get('login')
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
	pass

@app.route('/profile')
def profile():
	return render_template('profile.html', username = session.get('username'))

#бывшее /choose_your_room
@app.route('/room_list')
def room_list():
	return render_template('room_list.html', username = session.get('username'))

@app.route('/room/<room_id>')
def room():
	pass

@app.route('/rules')
def rules():
	return render_template('rules.html', is_enter=True)