# by Richi Rod AKA @richionline / falken20
# ./falken_drinks/models.py

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


# Flask-Login can manage user sessions. UserMixin will add Flask-Login attributes
# to the model so that Flask-Login will be able to work with it.
class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
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
    

class Drink(db.Model):
    __tablename__ = "drinks"
    drink_id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String(100), nullable=False)
    drink_water_percentage = db.Column(db.Integer, nullable=False, default=100)
    drink_alcohol_percentage = db.Column(db.Integer, nullable=False, default=0)
    drink_image = db.Column(db.String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<Drink ({self.drink_name} - {self.drink_water_percentage}% - {self.drink_alcohol_percentage}%)>"
    
    def __str__(self) -> str:
        return f"<Drink ({self.drink_name} - {self.drink_water_percentage}% - {self.drink_alcohol_percentage}%)>"
    
    def __init__(self, drink_name=None, drink_water_percentage=None, drink_alcohol_percentage=None, drink_image=None):
        self.drink_name = drink_name
        self.drink_water_percentage = drink_water_percentage
        self.drink_alcohol_percentage = drink_alcohol_percentage
        self.drink_image = drink_image
    
    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
    
    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    # The __declare_last__() hook allows definition of a class level function that is
    # automatically called by the MapperEvents.after_configured() event, which occurs
    # after mappings are assumed to be completed and the ‘configure’ step has finished.    
    @classmethod
    def __declare_last__(cls):
        ValidateString(cls.drink_name, False, True,
                       "Validate String: Drink name can't be empty or only spaces")
        ValidateInteger(cls.drink_water_percentage, False, True,
                        "Validate Integer: Drink water percentage should be a number between 0 and 100")
        ValidateLessThanOrEqual(cls.drink_water_percentage, 100, True,
                                "ValidateLessThanOrEqual: Drink water percentage should be a number between 0 and 100")
        ValidateGreaterThanOrEqual(cls.drink_water_percentage, 0, True,
                                   "ValidateGreaterThanOrEqual: Drink water percentage should be a number between 0 and 100")
        ValidateInteger(cls.drink_alcohol_percentage, False, True,
                        "Drink alcohol percentage should be a number between 0 and 100")
        ValidateLessThanOrEqual(cls.drink_alcohol_percentage, 100, True,
                                "Drink alcohol percentage should be a number between 0 and 100")
        ValidateGreaterThanOrEqual(cls.drink_alcohol_percentage, 0, True,
                                   "Drink alcohol percentage should be a number between 0 and 100")

    @validates('drink_name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Drink name can't be empty")
        return value
    
    @validates('drink_image')
    def validate_empty_string(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value
        
    @validates('drink_water_percentage', 'drink_alcohol_percentage')
    def validate_percentage(self, key, value):
        if value is None:
            raise ValueError("Drink percentage can't be empty")
        if not (0 <= value <= 100):
            raise ValueError(f"{key} must be between 0 and 100")
        return value
    
    @validates('drink_image')
    def validate_empty_string(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value
    

class DrinkLog(db.Model):
    __tablename__ = "drinks_logs"
    log_id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.drink_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    drink_total_quantity = db.Column(db.Integer, nullable=False)
    drink_water_quantity = db.Column(db.Integer, nullable=False)
    drink_alcohol_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<DrinkLog ({self.date_created} - {self.drink_total_quantity} - {self.drink_water_quantity} - {self.drink_alcohol_quantity})>"
    
    def __str__(self) -> str:
        return f"<DrinkLog ({self.date_created} - {self.drink_total_quantity} - {self.drink_water_quantity} - {self.drink_alcohol_quantity})>"
    
    def __init__(self, drink_id=None, user_id=None, drink_total_quantity=None, drink_water_quantity=None, drink_alcohol_quantity=None):
        self.drink_id = drink_id
        self.user_id = user_id
        self.drink_total_quantity = drink_total_quantity
        self.drink_water_quantity = drink_water_quantity
        self.drink_alcohol_quantity = drink_alcohol_quantity

    @validates('drink_id', 'user_id')
    def validate_id(self, key, value):
        if not value:
            raise ValueError("Drink ID or User ID can't be empty")
        return value
    
    @validates('drink_total_quantity', 'drink_water_quantity', 'drink_alcohol_quantity')
    def validate_quantity(self, key, value):
        if not value:
            raise ValueError("Drink quantity can't be empty")
        return value
    
    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    # The __declare_last__() hook allows definition of a class level function that is
    # automatically called by the MapperEvents.after_configured() event, which occurs
    @classmethod
    def __declare_last__(cls):
        ValidateInteger(cls.drink_total_quantity, False, True,
                        "Drink total quantity should be a number")
        ValidateInteger(cls.drink_water_quantity, False, True,
                        "Drink water quantity should be a number")
        ValidateInteger(cls.drink_alcohol_quantity, False, True,
                        "Drink alcohol quantity should be a number")
    
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
            app.config.from_object("falken_drinks.config.DevelopmentConfig")
        elif environment == "testing":
            app.config.from_object("falken_drinks.config.TestingConfig")
        elif environment == "production":
            app.config.from_object("falken_drinks.config.ProductionConfig")
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