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
    history = db.execute("SELECT ingredients, carboncost, carbonsaved FROM RECIPES WHERE id IN (?)", (history_ids,)).fetchall()
    return render_template("user/carbonhistory.html", recipes=history)

@bp.route("/")
@login_required
def user_info():
    return render_template("user/viewuser.html", user=g.user)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM USERS WHERE id = ?', (user_id,)
        ).fetchone()