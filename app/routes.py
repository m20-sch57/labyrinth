from flask import render_template, request, session, redirect, url_for
from app.room_namespace import RoomNamespace
from LabyrinthEngine import load_lrmap
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
    return render_template(url, username=session.get('username'), **kwargs)


@app.route('/')
@app.route('/index')
def index():
    return simple_render_template('index.html', reg_error=False)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if not db.users.have_user(username) or \
                not db.users.check_password(password, username):
            return redirect(url_for('login_failed'))

        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login_register/login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/change_login', methods=['POST', 'GET'])
def change_login():
    if request.method == 'POST':
        password = request.form.get("password")
        new_login = request.form.get("new_login")

        if not db.users.check_password(password):
            return redirect(url_for('change_login_failed'))

        db.users.set_username(new_login)
        session['username'] = new_login

        return redirect(url_for('profile'))

    return render_template('login_register/change_login.html')


@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    if request.method == 'POST':
        username = session['username']
        password = request.form.get('password')
        new_password = request.form.get('new_password')

        if not db.users.check_password(password):
            return redirect(url_for('change_password_failed'))

        db.users.set_password(new_password)

        return redirect(url_for('profile'))

    return render_template('login_register/change_password.html')


@app.route('/change_avatar', methods=['POST', 'GET'])
def change_avatar():
    if request.method == 'POST':
        username = session['username']
        avatar = request.form['avatar']

        answer = db.users.set_avatar(request.form['avatar'], username)

    return render_template('login_register/change_avatar.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('login')
        password = request.form.get('password')

        if not db.users.add(username, password):
            return redirect(url_for('register_failed'))

        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login_register/register.html')


@app.route('/login_failed')
def login_failed():
    return render_template('index.html', username=None, reg_error=True)


@app.route('/change_login_failed')
def change_login_failed():
    return render_template('login_register/change_login.html', error=True)


@app.route('/change_password_failed')
def change_password_failed():
    return render_template('login_register/change_password.html', error=True)


@app.route('/register_failed')
def register_failed():
    return render_template('login_register/register_failed.html')


@app.route('/profile')
@login_required
def profile():
    username = session.get('username')
    return simple_render_template('profile.html', ava='/static/images/avatars/'+db.users.get_avatar(username))


@app.route('/room_list/<page>', methods=['POST', 'GET'])
def room_list(page):
    if request.method == 'POST':
        room_id = request.form.get('join_button')
        return redirect(url_for('waiting_room', room_id=room_id))

    pages = db.rooms.page_by_page(6)
    pages_number = len(pages)
    page = int(page)

    return simple_render_template('rooms/room_list.html',
                                  pager=pages[page],
                                  first_page=0,
                                  prev_page=max(0, page - 1),
                                  next_page=min(pages_number - 1, page + 1),
                                  last_page=pages_number - 1)


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

        if event_type == 'change_name':
            name = request.form.get('new_name')
            db.rooms.set_name(room_id, name)
            emit('update', {'event': 'change_name', 'name': name},
                 broadcast=True, namespace='/'+room_id)

        elif event_type == 'change_description':
            description = request.form.get('new_description')
            db.rooms.set_description(room_id, description)
            emit('update', {'event': 'change_description', 'description': description},
                 broadcast=True, namespace='/'+room_id)

        elif event_type == 'start_game':
            labyrinth = load_lrmap('example', room_id, db.rooms.get(room_id).users)
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
        return simple_render_template('rooms/waiting_room.html', room=db.rooms.get(room_id), hide_header=True)


@app.route('/game_room/<room_id>', methods=['POST', 'GET'])
def game_room(room_id):
    username = session.get('username')
    labyrinth = db.lrm.get_labyrinth(room_id)
    if request.method == 'POST':
        event_type = request.headers.get('Event-Type')

        if event_type == 'update':
            msg = labyrinth.player_to_send(username)
            ats = labyrinth.get_active_player_ats()
            if labyrinth.get_active_player_username() == username:
                return json.dumps({'your_turn': 'yes', 'msg': msg, 'ats': ats})
            else:
                return json.dumps({'your_turn': 'no', 'msg': msg})

        elif event_type == 'turn':
            if labyrinth.get_active_player_username() == username:
                turn = request.form.get('turn')
                labyrinth.make_turn(turn)
                emit('update', {'event': 'player_make_turn'},
                     broadcast=True, namespace='/'+room_id)
    if labyrinth is None or username not in [user.get_username() for user in labyrinth.players_list]:
        return redirect(url_for('waiting_room', room_id=room_id))
    else:
        return simple_render_template('rooms/game_room.html', room=db.rooms.get(room_id), hide_header=True)
