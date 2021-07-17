from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .db import get_db
from .auth import login_required

bp = Blueprint('carboncalc', __name__, url_prefix='/carboncalc')

@bp.route("/leaderboard")
@login_required
def leaderboard():
    db = get_db()
    standings = db.execute('SELECT username, carbonsaved ORDERBY carbonsaved DESC LIMIT 10').fetchall()

    return render_template("carboncalc/leaderboard.html", standings=standings)

