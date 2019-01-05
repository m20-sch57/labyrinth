#encoding: utf-8

from app import app, dbase, socketio, labyrinths_list
from flask_socketio import emit, join_room, leave_room
from flask import render_template, request, session, redirect, url_for
from hashlib import sha1
import random
import string

from labyrinth_test import generate_labyrinth



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
    return render_template('login_register/login.html')


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
    return render_template('login_register/register.html')


@app.route('/login_failed')
def login_failed():
    return render_template('index.html', username= None, reg_error=True)


@app.route('/register_failed')
def register_failed():
    return render_template('login_register/register_failed.html')


@app.route('/profile')
def profile():
    username = session.get('username')
    return render_template('profile.html', username=session.get('username'))


@app.route('/room_list/<page>', methods=['POST', 'GET'])
def room_list(page):
    if request.method == 'POST':
        room_id = request.form.get('join_button')
        return redirect(url_for('waiting_room', room_id=room_id))
    return render_template('rooms/room_list.html', username=session.get('username'), pager=dbase.get_rooms_page_by_page()[int(page)])


@app.route('/rules')
def rules():
    return render_template('rules.html', is_enter=True)


@app.route('/create_room')
def create_room():
    def genereate_room_id(size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    room_id = genereate_room_id(8)
    dbase.add_room(room_id, session.get('username'))
    return redirect(url_for('waiting_room', room_id=room_id))


@app.route('/waiting_room/<room_id>', methods=['POST', 'GET'])
def waiting_room(room_id):
    if request.method == 'POST':
        event_type = request.headers.get('Event-Type')

        if event_type == 'change_name':
            name = request.form.get('new_name')
            dbase.set_room_name(room_id, name)
            emit('update', {'event': 'change_name', 'name': name}, broadcast=True, room=room_id, namespace='/wrws')

        elif event_type == 'change_description':
            description = request.form.get('new_description')
            dbase.set_description(room_id, description)
            emit('update', {'event': 'change_description', 'description': description}, broadcast=True, room=room_id, namespace='/wrws')

        elif event_type == 'start_game':
            labyrinth = generate_labyrinth(dbase.get_room_players(room_id))
            labyrinths_list.add_labyrinth(room_id, labyrinth)
            emit('update', {'event': 'start_game'}, broadcast=True, room=room_id, namespace='/wrws')
    
    username = session.get('username')
    if labyrinths_list.get_labyrinth(room_id) != None and username in list(map(lambda user: user.get_user_id(), labyrinths_list.get_labyrinth(room_id).field.players_list)):
        return redirect(url_for('game_room', room_id=room_id))
    else:
        return render_template('rooms/waiting_room.html', room=dbase.get_room(room_id), username=username, hide_header=True)


@app.route('/game_room/<room_id>', methods=['POST', 'GET'])
def game_room(room_id):
    username = session.get('username')
    labyrinth = labyrinths_list.get_labyrinth(room_id)
    if request.method == 'POST':
        event_type = request.headers.get('Event-Type')

        if event_type == 'update':
            msg = labyrinth.player_to_send(username)
            if labyrinth.get_active_player_user_id() == username:
                return 'y' + msg
            else:
                return 'n' + msg

        elif event_type == 'turn':
            if labyrinth.get_active_player_user_id() == username:
                turn = request.form.get('turn')
                labyrinth.make_turn(turn)
                emit('update', {'event': 'player_make_turn'}, broadcast=True, room=room_id, namespace='/grws')
    if labyrinth == None or username not in list(map(lambda user: user.get_user_id(), labyrinth.field.players_list)):
        return redirect(url_for('waiting_room', room_id=room_id))
    else:
        return render_template('rooms/game_room.html', room=dbase.get_room(room_id), username=username, hide_header=True)

@socketio.on('player join', namespace='/grws')  
@socketio.on('player join', namespace='/wrws')
def wrws_pj(msg):
    room_id = msg['room_id']
    username = session.get('username')

    join_room(room_id)
    dbase.add_player(room_id, username)
    emit('update', {'event': 'player_enter_or_leave', 'players': ','.join(dbase.get_room_players(room_id))}, broadcast=True, room=room_id, namespace='/wrws')

    session['room'] = room_id

@socketio.on('disconnect', namespace='/grws')
@socketio.on('disconnect', namespace='/wrws')
def wrws_pl():
    room_id = session.get('room')
    username = session.get('username')

    leave_room(room_id)
    dbase.remove_player(room_id, username)
    emit('update', {'event': 'player_enter_or_leave', 'players': ','.join(dbase.get_room_players(room_id))}, broadcast=True, room=room_id, namespace='/wrws')

    session.pop('room', None)