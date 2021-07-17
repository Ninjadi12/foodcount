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

@bp.route("/list")
@login_required
def list():
    return render_template("carboncalc/list.html", title = "Shopping List")

@bp.route('/home')
@login_required
def home():
    return render_template('homepage.html', title = "Home")