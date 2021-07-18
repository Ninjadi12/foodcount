from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .db import get_db
from .auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/history")
@login_required
def history():
    db = get_db()
    history_ids = ""
    if g.user['history'] is not None:
        history_ids = list(g.user['history'])
    history = db.execute("SELECT foodname, carboncost, carbonsaved FROM INGREDIENTS WHERE id IN (?)", (history_ids,)).fetchall()
    return render_template("user/carbonhistory.html", recipes=history)

@bp.route("/")
@login_required
def user_info():
    return render_template("user/viewuser.html", user=g.user)

def fetch_friends_list():
    db = get_db()
    values = db.execute(f"SELECT * FROM FRIENDS WHERE name = {session.get('user_id')}").fetchall()
    for value in values: 
        print(value['name2'])
    return values

@bp.route('/addfriends', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_id = session.get('user_id')
        username = request.form['username']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif db.execute(
            'SELECT id FROM FRIENDS WHERE name = ? AND name2 = ?', (user_id, username,)
        ).fetchone() is not None:
            error = f"You've already tried to add {username}"
        elif db.execute(
            'SELECT * FROM USERS WHERE name = ?', (username,)
        ).fetchone() is None:
              error = f"{username} doesn't exist"
        elif db.execute(
            'SELECT * FROM USERS WHERE id = ? AND name = ?', (user_id, username,)
        ).fetchone() is not None:
              error = f"You can't add yourself"
    
        if error is None:
            db.execute(
                'INSERT INTO FRIENDS (name, name2) VALUES (?, ?)',
                (user_id, username)
            )
            db.commit()

        flash(error)

    return render_template('user/addfriends.html', friends=fetch_friends_list())

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM USERS WHERE id = ?', (user_id,)
        ).fetchone()

import requests
import json

@bp.route("/testbonAPI")
def bonAPI():
    BONAPI_API_KEY = "bdec218560cbe2ab59aa2737f090cbc11280bb62"
    response = requests.get("https://www.bon-api.com/api/v1/ingredient/alternatives", headers={"Authorization": "Token " + BONAPI_API_KEY, "Content-type":"application/json"}, data="{\"ingredients\":\"['50ml cow milk', '0.5 cups of white rice']\"}").text
    unjsoned = json.loads(response)
    return unjsoned