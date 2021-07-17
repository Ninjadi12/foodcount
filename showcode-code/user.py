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
    history_ids = list(g["history"])
    history = db.execute("SELECT ingredients, carboncost, carbonsaved FROM RECIPES WHERE id IN (?)", (history_ids))
    render_template("carbonhistory.html", recipes=history)

@bp.route("/")
@login_required
def user_info():
    render_template("viewuser.html", user=g)