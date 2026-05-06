# by Richi Rod AKA @richionline / falken20
# ./falken_drinks/models.py

# ######################################################################
# This file is to set all the db models and use the ORM flask_sqlalchemy
# ######################################################################

# import logging
import sys
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import inspect

from .config import get_settings, now_cet_naive, today_cet
from .logger import Log

Log.info("***** Loading models.py")

db = SQLAlchemy()


# Flask-Login can manage user sessions. UserMixin will add Flask-Login attributes
# to the model so that Flask-Login will be able to work with it.
class User(UserMixin, db.Model):
    __tablename__ = "users"

    MAX_EMAIL_LENGTH = 100
    MAX_NAME_LENGTH = 100
    MAX_PASSWORD_LENGTH = 255

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.Date, nullable=False, default=today_cet)
    date_updated = db.Column(db.Date, nullable=False,
                             default=today_cet, onupdate=today_cet)

    def __repr__(self) -> str:
        return f"<User ({self.user_id} - {self.name or self.email})>"

    def __str__(self) -> str:
        return f"<User ({self.user_id} - {self.name or self.email})>"

    @validates('email', 'password')
    def validate_required_text(self, key, value):
        if value is None:
            raise ValueError(f'{key} cannot be empty')
        if isinstance(value, str) and not value.strip():
            raise ValueError(f'{key} cannot be blank')

        if not isinstance(value, str):
            return value

        value = value.strip()
        max_lengths = {
            'email': self.MAX_EMAIL_LENGTH,
            'password': self.MAX_PASSWORD_LENGTH,
        }
        max_length = max_lengths.get(key)
        if max_length is not None and len(value) > max_length:
            raise ValueError(f'{key} cannot be longer than {max_length} characters')

        return value

    @validates('name')
    def validate_name_optional(self, key, value):
        if value is None:
            return None
        if isinstance(value, str) and not value.strip():
            raise ValueError('name cannot be blank')
        if isinstance(value, str):
            value = value.strip()
            if len(value) > self.MAX_NAME_LENGTH:
                raise ValueError(f'name cannot be longer than {self.MAX_NAME_LENGTH} characters')
        return value

    # Check to use serialize()
    # How to serialize SqlAlchemy PostgreSQL query to JSON => https://stackoverflow.com/a/46180522
    def serialize(self):
        _excluded = {'password'}
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs
                if c.key not in _excluded}

    # We have to override the method get_id() to return the user_id because we use
    # the user_id instead of the id field. And Flask-Login uses the id field by default.
    def get_id(self):
        return str(self.user_id)


class Drink(db.Model):
    __tablename__ = "drinks"
    drink_id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String(100), nullable=False)
    drink_water_percentage = db.Column(db.Integer, nullable=False, default=100)
    drink_alcohol_percentage = db.Column(db.Integer, nullable=False, default=0)
    drink_image = db.Column(db.String(100), nullable=True)
    counts_as_water = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    def __repr__(self) -> str:
        return f"<Drink ({self.drink_name} - {self.drink_water_percentage}% - {self.drink_alcohol_percentage}%)>"

    def __str__(self) -> str:
        return f"<Drink ({self.drink_name} - {self.drink_water_percentage}% - {self.drink_alcohol_percentage}%)>"

    def __init__(
        self,
        drink_name=None,
        drink_water_percentage=None,
        drink_alcohol_percentage=None,
        drink_image=None,
        counts_as_water=None,
        user_id=None
    ):
        self.drink_name = drink_name
        self.drink_water_percentage = drink_water_percentage
        self.drink_alcohol_percentage = drink_alcohol_percentage
        self.drink_image = drink_image
        self.user_id = user_id
        # Default counts_as_water to False if drink has alcohol, otherwise True
        if counts_as_water is not None:
            self.counts_as_water = counts_as_water
        else:
            self.counts_as_water = False if (drink_alcohol_percentage and drink_alcohol_percentage > 0) else True

    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @validates('drink_name')
    def validate_name(self, key, value):
        if value is None or not str(value).strip():
            raise ValueError("Drink name can't be empty")
        return str(value).strip()

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
        if not isinstance(value, int):
            raise ValueError(f'{key} must be an integer')
        if not (0 <= value <= 100):
            raise ValueError(f"{key} must be between 0 and 100")
        return value


class DrinkLog(db.Model):
    __tablename__ = "drinks_logs"
    log_id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.drink_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=now_cet_naive)
    drink_total_quantity = db.Column(db.Integer, nullable=False)
    drink_water_quantity = db.Column(db.Integer, nullable=False)
    drink_alcohol_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<DrinkLog ({self.date_created} - {self.drink_total_quantity} "
            f"- {self.drink_water_quantity} - {self.drink_alcohol_quantity})>"
        )

    def __str__(self) -> str:
        return (
            f"<DrinkLog ({self.date_created} - {self.drink_total_quantity} "
            f"- {self.drink_water_quantity} - {self.drink_alcohol_quantity})>"
        )

    def __init__(
        self,
        drink_id=None,
        user_id=None,
        drink_total_quantity=None,
        drink_water_quantity=None,
        drink_alcohol_quantity=None,
        date_created=None
    ):
        self.drink_id = drink_id
        self.user_id = user_id
        self.drink_total_quantity = drink_total_quantity
        self.drink_water_quantity = drink_water_quantity
        self.drink_alcohol_quantity = drink_alcohol_quantity
        if date_created is not None:
            self.date_created = date_created

    @validates('drink_id', 'user_id')
    def validate_id(self, key, value):
        if value is None:
            raise ValueError("Drink ID or User ID can't be empty")
        return value

    @validates('drink_total_quantity', 'drink_water_quantity', 'drink_alcohol_quantity')
    def validate_quantity(self, key, value):
        Log.debug(f"Validating {key} with value {value} - {type(value)}")
        if value is None:
            raise ValueError(f"Drink quantity can't be empty: {key} - {value}")
        return value

    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class DailyHabit(db.Model):
    __tablename__ = 'daily_habits'

    TEXTURE_OPTIONS = ['hard', 'normal', 'soft', 'mushy', 'liquid']
    MIN_QUANTITY = 1
    MAX_QUANTITY = 5

    habit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=today_cet)
    quantity = db.Column(db.Integer, nullable=False)
    texture = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=now_cet_naive)

    def __repr__(self) -> str:
        return f"<DailyHabit ({self.habit_id} - {self.date} - qty:{self.quantity} - {self.texture})>"

    def __str__(self) -> str:
        return f"<DailyHabit ({self.habit_id} - {self.date} - qty:{self.quantity} - {self.texture})>"

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value is None:
            raise ValueError('quantity cannot be empty')
        value = int(value)
        if not (self.MIN_QUANTITY <= value <= self.MAX_QUANTITY):
            raise ValueError(f'quantity must be between {self.MIN_QUANTITY} and {self.MAX_QUANTITY}')
        return value

    @validates('texture')
    def validate_texture(self, key, value):
        if value is None or not str(value).strip():
            raise ValueError('texture cannot be empty')
        value = value.strip().lower()
        if value not in self.TEXTURE_OPTIONS:
            raise ValueError(f'texture must be one of: {", ".join(self.TEXTURE_OPTIONS)}')
        return value

    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def init_db_if_needed(app):
    """
    Automatically create database tables if they don't exist.
    Non-interactive version for development/testing environments.
    """
    try:
        with app.app_context():
            inspector = db.inspect(db.engine)
            existing_tables = set(inspector.get_table_names())
            
            # Define all table names that should exist
            required_tables = {'users', 'drinks', 'drinks_logs', 'daily_habits'}
            
            # If all required tables exist, nothing to do
            if required_tables.issubset(existing_tables):
                Log.debug("All required database tables already exist")
                return
            
            # Create all tables
            Log.info("Creating missing database tables...")
            db.create_all()
            db.session.commit()
            Log.info("Database tables initialized successfully")
    except Exception as err:
        Log.error("Error in init_db_if_needed", err, sys=sys)
        raise


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
# For execution in the console: python -m falken_drinks.models       #
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
