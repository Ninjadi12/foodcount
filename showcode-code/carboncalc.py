from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import requests

from .db import get_db
from .auth import login_required

BONAPI_API_KEY = "bdec218560cbe2ab59aa2737f090cbc11280bb62"

bp = Blueprint('carboncalc', __name__, url_prefix='/carboncalc')

@bp.route("/leaderboard")
@login_required
def leaderboard():
    db = get_db()
    standings = db.execute('SELECT name, carboncost, carbonsaved FROM USERS ORDER BY carbonsaved DESC LIMIT 10').fetchall()
    requests.post("https://test.eaternity.ch/api/", headers = {"authorization": "Basic aDRjSzR0SDBOT2c3NUhqZkszMzlLbE9scGEzOWZKenhYdw==", "Content-Type":"application/json"})
    return render_template("carboncalc/leaderboard.html", standings=standings)

def fetch_list():
    db = get_db()
    values = db.execute(f"SELECT * FROM INGREDIENTS WHERE userid = {session.get('user_id')}").fetchall()
    return values

@bp.route("/list", methods=('GET', 'POST'))
@login_required
def list():
    if request.method == 'GET':
        pass
    
    elif request.method == 'POST':
        food_type = request.form['food_type']
        food_name = request.form['food_name']
        quantity = request.form['quantity']


        
        db = get_db()
        
        db.execute(
            'INSERT INTO INGREDIENTS (foodtype, foodname, quantity, carboncost, userid) VALUES (?, ?, ?, ?, ?)',
            (food_type, food_name, quantity, 0,  session.get('user_id'))
        )
        db.commit()
        
        """
        if quantity is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('initial'))

        flash(error)


        elif db.execute(
            'SELECT id FROM USERS WHERE name = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO USERS (name, password, carboncost, carbonsaved) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), 0.0, 0.0)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)"""


    return render_template("carboncalc/list.html", title = "Shopping List", ingredients=fetch_list())

@bp.route('/home')
@login_required
def home():
    return render_template('carboncalc/homepage.html', title = "Home")