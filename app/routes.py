from app import app

@app.route('')
@app.route('/index')
def index():
	pass

@app.route('/login')
def login():
	pass

@app.route('/register')
def register():
	pass

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
	pass