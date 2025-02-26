import unittest
import os
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from datetime import date
from flask_sqlalchemy import SQLAlchemy


from falken_plants.app import create_app, settings
from falken_plants.models import db, User
from falken_plants.logger import Log

print("Loading basetest.py")

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseTestCase(unittest.TestCase):
    mock_user = {'email': 'python@mail.com',
                 'name': 'python', 'password': 'password'}
    mock_user_unknown = {'email': 'python@mail.com',
                         'name': 'python', 'password': 'error_password'}
    MOCK_PLANT = {'id': 100, 'name': 'test_plant_mock', 'name_tech': 'test_plant_mock', 'comment': 'test_plant_mock',
                  'watering_summer': 2, 'watering_winter': 2, 'spray': True, 'direct_sun': 2, 'image': '',
                  '_method': 'POST'}

    def setUp(self):
        Log.info("***** Setting up BaseTestCase...", style="red bold")

        # Create a new Flask application for testing
        self.app = create_app(settings.CONFIG_ENV['testing'])
        self.app.config['SECRET_KEY'] = 'secret_key_test'
        self.app.config['TESTING'] = True
        self.app.config['CONFIG_MODE'] = 'testing'
        self.app.config['ENV'] = 'testing'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = settings.CONFIG_ENV['testing'].SQLALCHEMY_DATABASE_URI
        Log.debug("***** BaseTest App config", style="red bold")
        # Log.info_dict(dict(self.app.config), level_log="DEBUG")
        Log.debug(
            f"SQLALCHEMY_DATABASE_URI: {self.app.config['SQLALCHEMY_DATABASE_URI']}", style="red bold")

        self.config_login()
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        try:
            Log.info("***** Tearing down BaseTestCase...", style="red bold")
            db.session.remove()
            db.drop_all()  
            self.app_context.pop()
        except Exception as e:
            Log.error("Error tearing down BaseTestCase", e, os)

    def config_login(self):
        # A user loader tells Flask-Login how to find a specific user from the ID that is stored in their
        # session cookie.
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(self.app)

        @login_manager.user_loader
        def load_user(user_id):
            # Since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

    @staticmethod
    def create_user(user: User = mock_user):
        new_user = User(email=user['email'], name=user['name'],
                        password=generate_password_hash(
                            user['password'], method='pbkdf2'),  # Before method='sha256'
                        date_created=date.today())
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login_http(self):
        return self.client.post('/login', data=self.mock_user, follow_redirects=True)
