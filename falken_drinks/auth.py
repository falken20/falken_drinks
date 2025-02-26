# by Richi Rod AKA @richionline / falken20
# ./falken_plants/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from datetime import date
import sys

from .models import db, User
from .logger import Log

print("Loading auth.py")

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    try:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        # If the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    except Exception as err:
        Log.error("Error in login_post", err=err, sys=sys)
        return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        date_created = date.today()

        # If this return a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            # By calling flash function, you can send a message to the next request
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name,
                        # password=generate_password_hash(password, 'pbkdf2'),  # Before method='sha256'
                        password=generate_password_hash(password, method='sha256'),  # Before method='sha256'
                        date_created=date_created)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    except Exception as err:
        Log.error("Error in signup_post", err=err, sys=sys)
        return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    logout_user()
    return redirect(url_for('auth.signup'))
