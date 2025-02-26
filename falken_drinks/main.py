# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sys

from .logger import Log
from .controllers import ControllerPlant

print("Loading main.py")

main = Blueprint('main', __name__)


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    all_plants = ControllerPlant.list_all_plants(current_user.id)

    # return redirect(url_for('main.view_all_plants'))
    return render_template('plant_list.html', plants=all_plants, message="")


@main.route('/show_grouped/')
@login_required
def show_grouped():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    all_plants = ControllerPlant.list_all_plants(current_user.id)

    return render_template('plant_list_group.html', plants=all_plants, message="")


@main.route("/profile", methods=['GET'])
@login_required
def profile():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    return render_template('profile.html', name=current_user.name, date_created=current_user.date_created)
