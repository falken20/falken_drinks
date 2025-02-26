# by Richi Rod AKA @richionline / falken20
# ./falken_plants/models.py

# ######################################################################
# This file is to set all the db models and use the ORM flask_sqlalchemy
# ######################################################################

# import logging
import sys
from datetime import date
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import inspect
from flask_validator import (ValidateString, ValidateInteger, ValidateEmail, ValidateLessThanOrEqual,
                             ValidateGreaterThanOrEqual, ValidateBoolean)

from .config import get_settings, print_settings_environment
from .logger import Log

print("Loading models.py")

db = SQLAlchemy()


class Plant(db.Model):
    __tablename__ = "t_plant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_tech = db.Column(db.String(100), nullable=True)
    comment = db.Column(db.String(200), nullable=True)
    # Frequency per month (1-4)
    watering_summer = db.Column(db.Integer, nullable=True, default=1)
    # Frequency per month (1-4)
    watering_winter = db.Column(db.Integer, nullable=True, default=2)
    spray = db.Column(db.Boolean, nullable=True, default=True)
    # Direct sun value 1: No, 2: Partial, 3: Yes
    direct_sun = db.Column(db.Integer, nullable=True, default=2)
    # image = db.Column(db.BLOB, nullable=True)
    image = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    date_updated = db.Column(db.Date, nullable=False,
                             default=date.today, onupdate=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"<Plant ({self.id} - {self.name} - {self.name_tech})>"

    def __str__(self) -> str:
        return f"<Plant ({self.id} - {self.name} - {self.name_tech})>"

    def __init__(self, name=None, name_tech=None, comment=None, watering_summer=1, watering_winter=2,
                 spray=True, direct_sun=2, image=None, user_id=None, date_created=date.today(),
                 date_updated=date.today()):
        self.name = name
        self.name_tech = name_tech
        self.comment = comment
        self.watering_summer = watering_summer
        self.watering_winter = watering_winter
        self.spray = spray
        self.direct_sun = direct_sun
        self.image = image
        self.user_id = user_id
        self.date_created = date_created
        self.date_updated = date_updated

    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    # The __declare_last__() hook allows definition of a class level function that is
    # automatically called by the MapperEvents.after_configured() event, which occurs
    # after mappings are assumed to be completed and the ‘configure’ step has finished.
    @classmethod
    def __declare_last__(cls):
        ValidateString(cls.name, False, True,
                       "Validate String: Plant name can't be empty or only spaces")
        ValidateInteger(cls.watering_summer, False, True,
                        "Validate Integer: Plant watering summer should be a number between 0 and 4")
        ValidateLessThanOrEqual(cls.watering_summer, 4, True,
                                "ValidateLessThanOrEqual: Plant watering summer should be a number between 0 and 4")
        ValidateGreaterThanOrEqual(cls.watering_summer, 0, True,
                                   "ValidateGreaterThanOrEqual: Plant watering summer should be a number between 0 and 4")
        ValidateInteger(cls.watering_winter, False, True,
                        "Plant watering winter should be a number between 0 and 4")
        ValidateLessThanOrEqual(cls.watering_winter, 4, True,
                                "Plant watering winter should be a number between 0 and 4")
        ValidateGreaterThanOrEqual(cls.watering_winter, 0, True,
                                   "Plant watering winter should be a number between 0 and 4")
        ValidateBoolean(cls.spray)
        ValidateInteger(cls.direct_sun, True, True,
                        "Plant direct sun should be a number between 1 and 3")
        ValidateLessThanOrEqual(cls.direct_sun, 3, True,
                                "Plant direct sun should be a number between 1 and 3")
        ValidateGreaterThanOrEqual(cls.direct_sun, 1, True,
                                   "Plant direct sun should be a number between 1 and 3")

    # SQLAlchemy has a built in helped method for using validations, validates(). Its a Server-side validation
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Plant name can't be empty")
        return value

    # Check to use @validates('name_tech', 'comment') => https://stackoverflow.com/a/57294872
    @validates('name_tech', 'comment')
    def validate_empty_string(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value

    # Check to use serialize()
    # How to serialize SqlAlchemy PostgreSQL query to JSON/dict => https://stackoverflow.com/a/46180522
    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Calendar(db.Model):
    __tablename__ = "t_calendar"

    date_calendar = db.Column(db.Date, primary_key=True)
    water = db.Column(db.Boolean, nullable=False, default=False)
    fertilize = db.Column(db.Boolean, nullable=False, default=False)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        't_plant.id'), nullable=False)

    def __repr__(self) -> str:
        return f"<Calendar ({self.date_calendar})>"


# Flask-Login can manage user sessions. UserMixin will add Flask-Login attributes
# to the model so that Flask-Login will be able to work with it.
class User(UserMixin, db.Model):
    __tablename__ = "t_user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    date_updated = db.Column(db.Date, nullable=False,
                             default=date.today, onupdate=date.today)

    def __repr__(self) -> str:
        return f"<User ({self.id} - {self.name})>"

    def __str__(self) -> str:
        return f"<User ({self.id} - {self.name})>"

    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    # The __declare_last__() hook allows definition of a class level function that is
    # automatically called by the MapperEvents.after_configured() event, which occurs
    # after mappings are assumed to be completed and the ‘configure’ step has finished.
    @classmethod
    def __declare_last__(cls):
        ValidateEmail(cls.email, False, True,
                      "User email can't be empty or only spaces")
        ValidateString(cls.name, False, True,
                       "User name can't be empty or only spaces")
        ValidateString(cls.password, False, True,
                       "User password can't be empty or only spaces")

    # Check to use serialize()
    # How to serialize SqlAlchemy PostgreSQL query to JSON => https://stackoverflow.com/a/46180522
    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def init_db(app):
    """
    Main process to create the needed tables for the application
    """
    Log.info("Init DB process starting...")

    try:
        if input("Could you drop the tables if they exist(y/n)?\n") in ["Y", "y"]:
            Log.info("Dropping tables...")
            with app.app_context():
                db.drop_all()
            Log.info("Tables dropped")

        if input("Could you create the tables(y/n)?\n") in ["Y", "y"]:
            Log.info("Creating tables...")
            with app.app_context():
                db.create_all()
            Log.info("Tables created")

        with app.app_context():
            db.session.commit()

        Log.info("Process finished succesfully")

    except Exception as err:  # pragma: no cover
        # Log.error(f"Execution Error in init_db: {err}", exc_info=True)
        Log.error("Execution Error in init_db", err, sys=sys)


######################################################################
# For execution in the console: python -m falken_plants.models       #
######################################################################
# FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
# logging.basicConfig(level=logging.INFO, format=FORMAT)

if __name__ == '__main__':  # pragma: no cover # To doesn't check in tests
    try:
        Log.info("Preparing app vars...")
        app = Flask(__name__)

        # Set environment vars
        settings = get_settings()
        app.config.from_object(settings)

        # Select environment to create the tables
        environment = input(
            "Select the environment to create the tables (development, testing, production, exit):\n")
        if environment == "development":
            app.config.from_object("falken_plants.config.DevelopmentConfig")
        elif environment == "testing":
            app.config.from_object("falken_plants.config.TestingConfig")
        elif environment == "production":
            app.config.from_object("falken_plants.config.ProductionConfig")
        elif environment == "exit":
            Log.info("Process finished")
            exit(0)
        else:
            Log.warning(
                f"Invalid input: Environment not found '{environment}'")
            raise ValueError(
                f"Invalid input: Environment not found '{environment}'")

        # app.config.from_object(settings.CONFIG_ENV[settings.CONFIG_MODE])
        app.config['TEMPLATE_AUTO_RELOAD'] = True

        settings.CONFIG_MODE = environment
        Log.info(f"Running in '{environment}' mode", style="red bold")
        Log.debug(f"Debug: {app.config['DEBUG']}")
        Log.debug(f"Testing: {app.config['TESTING']}")
        Log.info(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

        db.init_app(app)
        init_db(app)

    except Exception as err:
        Log.error("Error in models.py", err, sys=sys)
        exit(1)