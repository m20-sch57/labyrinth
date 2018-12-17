from app import app, dbase
from flask import render_template, request, session, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', username=session.get('username'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        user = dbase.get_user(username)
        print(user)
        if user is None:
            return redirect(url_for('login_failed'))

        if user[1] != password:
            return redirect(url_for('login_failed'))

        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        user = dbase.get_user(username)
        if user is not None:
            return redirect(url_for('register_failed'))

        dbase.add_user(username, password)

        session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login_failed')
def login_failed():
    return render_template('login_failed.html')


@app.route('/register_failed')
def register_failed():
    return render_template('register_failed.html')


@app.route('/profile')
def profile():
    username = session.get('username')
    user = dbase.get_user(username)
    return render_template('profile.html', username=session.get('username'))


#бывшее /choose_your_room
@app.route('/room_list', methods=['POST', 'GET'])
def room_list():
    if request.method == 'POST':
        joinlink = request.form.get('joinlink')
        players = request.form.get('players')
        username = session.get('username')

        dbase.add_room(joinlink, players, '', username)
    return render_template('room_list.html', username=session.get('username'))


@app.route('/room/<room_id>')
def room(room_id):
    current_room = dbase.get_room_by_link(room_id)
    print(room_id)
    print(current_room)
    return render_template('room_list.html', username=session.get('username'))


@app.route('/rules')
def rules():
    return render_template('rules.html', is_enter=True)
