#encoding: utf-8

from app import app, dbase, socketio
from flask_socketio import emit, join_room, leave_room
from flask import render_template, request, session, redirect, url_for
from hashlib import sha1
import random
import string


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
        room_id = request.form.get('join_button')
        return redirect(url_for('waiting_room', room_id=room_id))
    return render_template('room_list.html', username=session.get('username'), pager=dbase.get_rooms_page_by_page()[int(page)])


@app.route('/rules')
def rules():
    return render_template('rules.html', is_enter=True)


@app.route('/create_room')
def create_room():
    def genereate_room_id(size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    room_id = genereate_room_id(8)
    dbase.add_room(room_id, 4, '', session.get('username'))
    return redirect(url_for('waiting_room', room_id=room_id))

@app.route('/waiting_room/<room_id>')
def waiting_room(room_id):
    return render_template('waiting_room.html', room_id=room_id)

@socketio.on('player join', namespace='/wrws')
def wrws_pj(msg):
    room_id = msg['room_id']
    session['room'] = room_id
    join_room(session.get('room')) 
    # print('{} enter into the room {}'.format(session.get('username'), session.get('room')))
    emit('update', {'room_id': session.get('room'), 'event': session.get('username') + ' join'}, broadcast = True, room=session.get('room'))

@socketio.on('disconnect', namespace='/wrws')
def wrws_pl():
    # print('{} leave room {}'.format(session.get('username'), session.get('room')))
    leave_room(session.get('room'))
    emit('update', {'room_id': session.get('room'), 'event': session.get('username') + ' leave'}, broadcast = True, room=session.get('room'))
    session.pop('room', None)
