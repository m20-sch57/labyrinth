#encoding: utf-8

from app import app, dbase
from flask import render_template, request, session, redirect, url_for
from hashlib import sha1


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', username=session.get('username'), reg_error=False)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if not dbase.user_login_in_table(username) or dbase.get_user_password_hash(username) != sha1(password.encode('utf-8')).hexdigest():
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

        if not dbase.add_user(username, sha1(password.encode('utf-8')).hexdigest()):
            return redirect(url_for('register_failed'))

        session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login_failed')
def login_failed():
    return render_template('index.html', username= None, reg_error=True)


@app.route('/register_failed')
def register_failed():
    return render_template('register_failed.html')


@app.route('/profile')
def profile():
    username = session.get('username')
    return render_template('profile.html', username=session.get('username'))


@app.route('/room_list/<page>', methods=['POST', 'GET'])
def room_list(page):
    if request.method == 'POST':
        joinlink = request.form.get('joinlink')
        players = request.form.get('players')
        username = session.get('username')
        if players:
            dbase.add_room(joinlink, username)
        else:
            joinlink = request.form.get('roomlink')
        return redirect(url_for('room', room_id=joinlink))
    # pages = dbase.get_pages()
    # pagen = int(page)
    return render_template('room_list.html', username=session.get('username'), pager=dbase.get_rooms_page_by_page[int(page)])


@app.route('/room/<room_id>')
def room(room_id):
    username = session.get('username')
    dbase.add_player(room_id, username)
    return render_template('room_list.html', username=session.get('username'))


@app.route('/rules')
def rules():
    return render_template('rules.html', is_enter=True)
