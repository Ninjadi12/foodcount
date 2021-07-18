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
    standings = db.execute('SELECT name, carboncost, carbonsaved FROM USERS WHERE carboncost > 0 ORDER BY carboncost ASC LIMIT 10;').fetchall()
    requests.post("https://test.eaternity.ch/api/", headers = {"authorization": "Basic aDRjSzR0SDBOT2c3NUhqZkszMzlLbE9scGEzOWZKenhYdw==", "Content-Type":"application/json"})
    pic1 = os.path.join("../" + current_app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template("carboncalc/leaderboard.html", standings=standings, title = "FUCounter | Leaderboard", logo= pic1)

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
    "Brown Rice": 2.16,
    "Chickpeas": 0.64,
    "Peas": 0.29,
    "Yoghurt": 2.2,

}

alternatives = {
    "Butter": "Margarine",
    "White Rice": "Brown Rice",
    "Beef": "Pork",
    "Turkey": "Chicken"
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

def add_food():
    food_type = request.form['food_type']
    food_name = request.form['food_name']
    quantity = request.form['quantity']
    error = ""

    if food_name in co2:
        food_co2 = co2[food_name] * int(quantity)
    else:
        error = "Ingredient not implemented"
        print(error)
    user_id = session.get('user_id')

    if error == "":
        db = get_db()
    
        db.execute(
            'INSERT INTO INGREDIENTS (foodtype, foodname, quantity, carboncost, userid) VALUES (?, ?, ?, ?, ?)',
            (food_type, food_name, quantity, food_co2,  user_id)
        )

        db.execute(f'UPDATE USERS SET carboncost = {get_avg_carbon()} WHERE id = \"{user_id}\"')
        db.commit()
    return error

def use_alternative():
    db = get_db()
    user_id = session.get('user_id')

    # get selected ingredient
    
    # doesn't work with multiple items of same type!
    original_ingredient = request.form['foodname']
    original = db.execute(f"SELECT * FROM INGREDIENTS WHERE userid = \"{user_id}\" AND foodname = \"{original_ingredient}\"").fetchall()[0]
    alternative = alternatives[original_ingredient]
    alternative_co2 = co2[alternative] * int(original["quantity"])
    original_co2 = original["carboncost"]

    

    # doesn't work with alternative being different type
    # alternative must have carbon implemented!
    record_id = request.form["id"]
    db.execute(f'UPDATE INGREDIENTS SET foodname = \"{alternative}\", carboncost = {alternative_co2} WHERE userid = \"{user_id}\" AND foodname = \"{original_ingredient}\" AND id = \"{record_id}\"')
    originalcarbon = db.execute(f"SELECT carboncost FROM USERS WHERE id = \"{user_id}\"").fetchall()[0]['carboncost']
    db.execute(f'UPDATE USERS SET carbonsaved = {original_co2 - alternative_co2}, carboncost = {get_avg_carbon()} WHERE id = \"{user_id}\"')

    db.commit()  
    return (1 - alternative_co2 / (co2[original_ingredient] * int(original["quantity"]))) * 100
    # update ingredient db
    # update user db

def delete():
    db = get_db()
    user_id = session.get('user_id')

    record_id = request.form["id"]

    original_ingredient = request.form['foodname']
    db.execute(f"DELETE FROM INGREDIENTS WHERE userid = \"{user_id}\" AND foodname = \"{original_ingredient}\" AND id = \"{record_id}\"")
  
    db.commit()    


@bp.route("/list", methods=('GET', 'POST'))
@login_required
def list():
    error = ""
    saving = 0
    id = -1
    if request.method == 'POST':
        if 'food_type' in request.form:
            error = add_food()
        else:
            if request.form['type'] == 'del':
                delete()
            else:
                saving = use_alternative()
                id = int(request.form["id"])
    
    pic1 = os.path.join("../" + current_app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template("carboncalc/list.html", title = "FUCounter | Shopping List", ingredients=fetch_list(), error=error, alternatives=alternatives, co2=co2, saving=saving, id=id, logo=pic1)
    
@bp.route('/home')
@login_required
def home():
    pic1 = os.path.join("../" + current_app.config['UPLOAD_FOLDER'], 'logo.png')
    pic2 = os.path.join("../" + current_app.config['UPLOAD_FOLDER'], 'badge.png')
    pic3 = os.path.join("../" + current_app.config['UPLOAD_FOLDER'], 'coin.png')
    return render_template('carboncalc/homepage.html', title = "FUCounter | Home", logo = pic1, Badge = pic2, coin=pic3)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM USERS WHERE id = ?', (user_id,)
        ).fetchone()