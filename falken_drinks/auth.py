# by Richi Rod AKA @richionline / falken20
# ./falken_plants/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import sys

from .config import today_cet
from .models import db, User
from .controllers import ControllerDrinks
from .logger import Log

Log.info("***** Loading auth.py")

auth = Blueprint('auth', __name__)

# Fallback hash used to prevent user enumeration via timing differences
_DUMMY_HASH = generate_password_hash('__dummy_timing_guard__', method='pbkdf2:sha256')

# Basic email format pattern (server-side validation)
_EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

# Rate limiter instance (shares storage with app limiter)
_limiter = Limiter(get_remote_address, storage_uri='memory://')


@auth.route('/login')
def login():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
@_limiter.limit('10 per minute')
def login_post():
    try:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not _EMAIL_PATTERN.match(email):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        # Always run hash comparison to prevent user-enumeration via timing
        candidate_hash = user.password if user else _DUMMY_HASH
        password_ok = check_password_hash(candidate_hash, password)

        if not user or not password_ok:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

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
@_limiter.limit('5 per minute')
def signup_post():
    try:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        email = request.form.get('email', '').strip().lower()
        name = request.form.get('name') or None
        password = request.form.get('password', '')
        date_created = today_cet()

        # Validate email format
        if not _EMAIL_PATTERN.match(email):
            flash('Please enter a valid email address.')
            return redirect(url_for('auth.signup'))

        # Server-side password strength validation
        if len(password) < 8:
            flash('Password must be at least 8 characters long.')
            return redirect(url_for('auth.signup'))

        # If this return a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        # if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash('Email address already exists. Go to login page.')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, name=name,
                        password=generate_password_hash(password, method='pbkdf2:sha256'),
                        date_created=date_created)

        db.session.add(new_user)
        db.session.commit()

        ControllerDrinks.seed_default_drinks(new_user.user_id)

        return redirect(url_for('auth.login'))
    except Exception as err:
        db.session.rollback()
        Log.error("Error in signup_post", err=err, sys=sys)
        flash('Error creating your account. Please try again.')
        return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    logout_user()
    return redirect(url_for('auth.login'))
