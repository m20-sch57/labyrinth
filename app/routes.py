#encoding: utf-8

from app import app, dbase
from flask import render_template, request, session, redirect, url_for
from labyrinth_test import MyLab

import sys
sys.path.append('../')
MyLab.ready()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', username=session.get('username'), reg_error=False)


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
    return render_template('index.html', username= None, reg_error=True)


@app.route('/register_failed')
def register_failed():
    return render_template('register_failed.html')


@app.route('/profile')
def profile():
    username = session.get('username')
    user = dbase.get_user(username)
    return render_template('profile.html', username=session.get('username'))


#Ð±Ñ‹Ð²ÑˆÐµÐµ /choose_your_room
@app.route('/room_list/<page>', methods=['POST', 'GET'])
def room_list(page):
    if request.method == 'POST':
        joinlink = request.form.get('joinlink')
        players = request.form.get('players')
        username = session.get('username')
        if players:
            dbase.add_room(joinlink, players, '', username)
        else:
            joinlink = request.form.get('roomlink')
        return redirect(url_for('room', room_id=joinlink))
    pages = dbase.get_pages()
    pagen = int(page)
    return render_template('room_list.html', username=session.get('username'), pager=pages[pagen])


@app.route('/room/<room_id>')
def room(room_id):
    current_room = dbase.get_room_by_link(room_id)
    print(room_id)
    print(current_room)
    return render_template('room_list.html', username=session.get('username'))


@app.route('/rules')
def rules():
    return render_template('rules.html', is_enter=True)


@app.route('/single_room')
def single_room():
    return render_template('single_room.html', head='single mode')


@app.route('/single_turn/<turn>')
def single_turn(turn):
    print(turn)
    msg = MyLab.make_turn(turn)
    print('player position: ', MyLab.get_active_player().get_parent_id().number, MyLab.get_active_player().get_parent_id().type)
    return msg
