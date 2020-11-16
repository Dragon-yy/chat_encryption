from flask import Blueprint, redirect, url_for
from flask_login import logout_user

route_logout = Blueprint('logout', __name__)


@route_logout.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login.login'))
