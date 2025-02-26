# by Richi Rod AKA @richionline / falken20
# ./falken_plants/urls.py
import sys
from flask import request, redirect, Blueprint, render_template
from flask_login import login_required, current_user
# import pprint

from .controllers import ControllerPlant
from .logger import Log

print("Loading urls.py")

urls = Blueprint('urls', __name__)


# API Plants

# PUT is not neccesary and not supported by HTML
@urls.route("/plants", methods=['GET', 'POST', 'PUT'])
@login_required
def list_create_plants():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    Log.debug(f"Current user: {current_user}")

    if request.method == 'GET':
        all_plants = ControllerPlant.list_all_plants(current_user.id)
        return render_template('plant_list.html', plants=all_plants, message="")
    elif request.method == 'POST':
        return post_plant()
    else:
        return "Method not allowed", 405


@urls.route("/plants/<int:plant_id>", methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_update_delete_plants(plant_id):
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    Log.debug(f"Current user: {current_user}")

    if request.method == 'GET':
        plant = ControllerPlant.get_plant(plant_id)
        return render_template('plant_form.html', plant=plant, form_method="GET")
    elif request.method == 'PUT':
        return put_plant(plant_id)
    elif request.method == 'DELETE':
        ControllerPlant.delete_plant(plant_id)
        all_plants = ControllerPlant.list_all_plants(current_user.id)
        return render_template('plant_list.html', plants=all_plants, message="")
    else:
        return "Method not allowed", 405


@urls.route("/plants/<int:plant_id>/delete", methods=['GET'])
@login_required
def delete_plant(plant_id: int):
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    Log.debug(f"Current user: {current_user}")

    ControllerPlant.delete_plant(plant_id)
    Log.info(f"Plant deleted: {plant_id}")
    all_plants = ControllerPlant.list_all_plants(current_user.id)
    return render_template('plant_list.html', plants=all_plants, message="")


# API Pages Plants

@urls.route("/plants/create", methods=['GET'])
@login_required
def view_create_plant():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    Log.debug(f"Current user: {current_user}")

    return render_template('plant_form.html', plant=None, form_method="POST")


@urls.route("/plants/update/<int:plant_id>", methods=['GET'])
@login_required
def view_update_plant(plant_id: int):
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    Log.debug(f"Current user: {current_user}")

    plant = ControllerPlant.get_plant(plant_id)
    Log.debug(f"Plant to update: {plant}")

    return render_template('plant_form.html', plant=plant, form_method="PUT")


# Auxiliary methods API Plants

@login_required
def post_plant():
    # Because HTML doesn't support PUT method, we use a hidden field to know if its a PUT method
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    try:
        Log.info(f"Hidden Method HTTP: {request.form['_method']}")
        plant = None
        # Log.debug(f"Request form: {request.form}")
        Log.debug(f"Request form: {request.form}")
        # pprint.pprint(request.form)

        # Because HTML doesn't support PUT method, we use a hidden field to know if its a PUT method
        if request.form['_method'] == "PUT":
            Log.info("Hidden PUT method: Update the plant")
            # Log.info(f"Its a PUT method, redirect to update plant API: /plants/{request.form['id']}")
            # return redirect(f"/plants/{request.form['id']}")
            # return redirect(url_for('main.put_plant', plant_id=request.form['id'], method='PUT'))
            # put_plant(request.form['id'])

            plant = ControllerPlant.update_plant(request.form, current_user.id)
            Log.info(f"Plant updated: {plant}")
        else:  # Its a POST method
            plant = ControllerPlant.create_plant(request.form, current_user.id)
            Log.info(f"Plant created: {plant}")
    except Exception as e:
        Log.error("Error creating/update plant", err=e, sys=sys)
        return render_template('plant_form.html', plant=plant, form_method=request.form['_method'], error=e)

    return redirect("/plants")


@login_required
def put_plant(plant_id: int):
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.info(f"Method HTTP: {request.method}")
    Log.debug(f"Current user: {current_user}")

    try:
        # Log.debug(f"Request form: {request.form}")
        Log.debug(f"Request form: {request.form}")
        # pprint.pprint(request.form)

        plant_id = plant_id if plant_id else request.form['plant_id']
        plant = ControllerPlant.update_plant(request.form, current_user.id)
        Log.info(f"Plant updated: {plant}")
    except Exception as e:
        Log.error("Error updating plant", err=e, sys=sys)
        return render_template('plant_form.html', error=e)

    return render_template('plant_list.html')
