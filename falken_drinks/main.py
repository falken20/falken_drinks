# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import date
import sys

from .logger import Log
from .controllers import ControllerDrinkLogs

Log.info("***** Loading app.py")

main = Blueprint('main', __name__)


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    # Get daily consumption data for the current user
    daily_consumption = ControllerDrinkLogs.get_daily_consumption(current_user.user_id)
    
    return render_template('home.html', daily_consumption=daily_consumption)


@main.route("/profile", methods=['GET'])
@login_required
def profile():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    return render_template('profile.html', name=current_user.name, date_created=current_user.date_created)
