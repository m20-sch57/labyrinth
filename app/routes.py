from flask import render_template, request, session, redirect, url_for
from app.room_namespace import RoomNamespace
from labyrinth_engine import load_map
from app import app, db, socketio
from flask_socketio import emit
from functools import wraps
import random
import string
import json





'''
help functions
'''

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('index'))
        else:
            return f(*args, **kwargs)

    return wrapped


def simple_render_template(url, **kwargs):
    username = session.get('username')
    ava_prefix = '/static/images/avatars/'
    if username is not None:
        user = db.users.get_by_name(username)
        user_ava = ava_prefix + db.users.get_avatar(username)
    else:
        user = None
        user_ava = None
    return render_template(url, username=username, user_ava=user_ava, user=user, args=request.args, **kwargs)

def redirect_with_args(url = None, **kwargs):
    if url is None:
        url = request.referrer.split('?')[0]
    return redirect(url+'?'+ '&'.join([str(k)+'='+str(v) for k, v in kwargs.items()]))


@app.route('/')
@app.route('/index')
def index():
    return simple_render_template('index.html', homepage=True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if not db.users.have_user(username) or \
                not db.users.check_password(password, username):
            return redirect_with_args(form = 'login', result = 'false')

        session['username'] = username
        return redirect(url_for('index'))
    return simple_render_template('login_register/login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return simple_render_template('profile/profile.html', form = request.args.get('form'), result = request.args.get('result'))


@app.route('/profile/change_login', methods=['POST', 'GET'])
def change_login():
    if request.method == 'POST':
        new_login = request.form.get("new_login")
        db.users.set_username(new_login)
        session['username'] = new_login

        return redirect_with_args(form='login', result='true')

    return simple_render_template('profile/change_login.html', form = request.args.get('form'), result = request.args.get('result'))


@app.route('/profile/change_password', methods=['POST', 'GET'])
def change_password():
    if request.method == 'POST':
        username = session['username']
        password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if not db.users.check_password(password):
            return redirect_with_args(form='password', result='false')

        db.users.set_password(new_password)
        return redirect_with_args(form='password', result='true')

    return simple_render_template('profile/change_password.html', form = request.args.get('form'), result = request.args.get('result'))


@app.route('/profile/change_avatar', methods=['POST', 'GET'])
def change_avatar():
    if request.method == 'POST':
        username = session['username']
        avatar = request.form['new_avatar']
        answer = db.users.set_avatar(avatar, username)
        if answer.ok:
            return redirect_with_args(form='change_avatar', result='true')
        else:
            return redirect_with_args(form='change_avatar', result='false')
    return simple_render_template('profile/change_avatar.html', form = request.args.get('form'), result = request.args.get('result'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if not db.users.add(username, password).ok:
            return redirect_with_args(form='register', result='false')

        session['username'] = username
        return redirect(url_for('index'))
    return simple_render_template('login_register/register.html')


@app.route('/add_map', methods=['POST', 'GET'])
def add_map():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        creator = session.get('username')
        map_json = request.form.get('map_json')

        db.maps.add(name, creator, description, map_json)

        return redirect(url_for('index'))
    return simple_render_template('add_map.html')


@app.route('/room_list/<page>', methods=['POST', 'GET'])
def room_list(page):
    if request.method == 'POST':
        room_id = request.form.get('join_button')
        return redirect(url_for('waiting_room', room_id=room_id))

    rooms = db.rooms.get_all()

    return simple_render_template('rooms/room_list.html', rooms = rooms)


@app.route('/rules')
def rules():
    return simple_render_template('rules.html')


@app.route('/create_room')
@login_required
def create_room():
    def genereate_room_id(size):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    room_id = genereate_room_id(8)
    db.rooms.add(room_id, session.get('username'))
    socketio.on_namespace(RoomNamespace('/' + room_id))

    return redirect(url_for('waiting_room', room_id=room_id))


@app.route('/waiting_room/<room_id>', methods=['POST', 'GET'])
@login_required
def waiting_room(room_id):
    if request.method == 'POST':
        event_type = request.headers.get('Event-Type')

        if event_type == 'change_settings':
            name = request.form.get('name')
            description = request.form.get('description')
            map_id = request.form.get('map_id')
            if name:
                db.rooms.set_name(room_id, name)
            if description:
                db.rooms.set_description(room_id, description)
            if map_id:
                lr_map = db.maps.get(map_id).to_dict()
            else:
                lr_map = None
            db.rooms.set_map(room_id, map_id)
            room = db.rooms.get(room_id)
            emit('update', {'event': 'change_settings', 'description': room.description, 
                 'name': room.name, 'map': lr_map},
                 broadcast=True, namespace='/'+room_id)

        elif event_type == 'start_game':
            imagepath='/static/images/button_images/'
            map_id = db.rooms.get(room_id).map_id
            labyrinth = load_map(db.maps.get(map_id).map, db.rooms.get(room_id).users, imagepath=imagepath)
            db.lrm.add_labyrinth(room_id, labyrinth)
            emit('update', {'event': 'start_game'},
                 broadcast=True, namespace='/'+room_id)

        elif event_type == 'delete_room':
            emit('update', {'event': 'delete_room'},
                 broadcast=True, namespace='/'+room_id)
            db.rooms.delete(room_id)

    username = session.get('username')
    labyrinth = db.lrm.get_labyrinth(room_id)
    if labyrinth is not None and username in [user.get_username() for user in labyrinth.players_list]:
        return redirect(url_for('game_room', room_id=room_id))
    elif db.rooms.get(room_id) is None:
        return redirect(url_for('room_list', page=0))
    else:
        return simple_render_template('rooms/waiting_room.html', room=db.rooms.get(room_id), hide_header=True, maps=db.maps.get_all())


@app.route('/game_room/<room_id>', methods=['POST', 'GET'])
def game_room(room_id):
    username = session.get('username')
    labyrinth = db.lrm.get_labyrinth(room_id)
    if request.method == 'POST':
        event_type = request.headers.get('Event-Type')

        if event_type == 'update':
            bar = labyrinth.get_bars(username)
            btn = labyrinth.get_buttons()
            msg = labyrinth.player_to_send(username)
            ats = labyrinth.get_active_player_ats()
            if labyrinth.get_active_player_username() == username:
                return json.dumps({'your_turn': 'yes', 'msg': msg, 'ats': ats, 'bars': bar, 'buttons': btn})
            else:
                return json.dumps({'your_turn': 'no', 'msg': msg, 'bars': bar})

        elif event_type == 'turn':
            if labyrinth.get_active_player_username() == username:
                turn = request.form.get('turn')
                labyrinth.make_turn(turn)
                emit('update', {'event': 'player_make_turn'},
                     broadcast=True, namespace='/'+room_id)
    if labyrinth is None or username not in [user.get_username() for user in labyrinth.players_list]:
        return redirect(url_for('waiting_room', room_id=room_id))
    else:
        return simple_render_template('rooms/game_room.html', room=db.rooms.get(room_id))
