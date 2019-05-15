from flask import request, render_template, session
from functools import wraps
from app import db

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('username') is None and request.method == 'GET':
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