from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
import os

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
    return render_template("carboncalc/leaderboard.html", standings=standings, title = "FUCounter | Leaderboard")

def fetch_list():
    db = get_db()
    values = db.execute(f"SELECT * FROM INGREDIENTS WHERE userid = {session.get('user_id')}").fetchall()
    return values

co2 = {
    "Butter": 12.1,
    "Margarine": 3.3,
    "Lamb": 39.2,
    "Beef": 27,
    "Cheddar Cheese": 13.5,
    "Pork": 12.1,
    "Turkey": 10.9,
    "Chicken": 6.9,
    "Lentils": 0.9,
    "White Rice": 2.7,
    "Brown Rice": 2.16
}

def get_avg_carbon():
    db = get_db()
    values = db.execute(f"SELECT * FROM INGREDIENTS WHERE userid = {session.get('user_id')}").fetchall()
    
    cost = 0
    quantity = 0
    for ingredient in values:
        cost += ingredient["carboncost"]
        quantity += ingredient["quantity"]
    if quantity > 0:
        avgcost = cost / quantity
    else:
        avgcost = 0
    
    return avgcost


@bp.route("/list", methods=('GET', 'POST'))
@login_required
def list():
    if request.method == 'POST':
        food_type = request.form['food_type']
        food_name = request.form['food_name']
        quantity = request.form['quantity']
        food_co2 = co2[food_name] * int(quantity)
        user_id = session.get('user_id')

        
        db = get_db()
        
        db.execute(
            'INSERT INTO INGREDIENTS (foodtype, foodname, quantity, carboncost, userid) VALUES (?, ?, ?, ?, ?)',
            (food_type, food_name, quantity, food_co2,  user_id)
        )

        db.execute(f'UPDATE USERS SET carboncost = {get_avg_carbon()} WHERE id = {user_id}')
        db.commit()
        

    get_avg_carbon()
    return render_template("carboncalc/list.html", ingredients=fetch_list(), title = "FUCounter | Shopping List")

@bp.route('/home')
@login_required
def home():
    pic1 = os.path.join("../" + current_app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('carboncalc/homepage.html', title = "FUCounter | Home", logo = pic1)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM USERS WHERE id = ?', (user_id,)
        ).fetchone()