# by Richi Rod AKA @richionline / falken20
# ./falken_plants/config.py

# Library that uses type annotation to validate data and manage settings.
# from pydantic import BaseSettings # Old version
import os
import sys
import toml
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic.v1 import BaseSettings
# from pydantic_settings import BaseSettings # New version
# import pyshorteners

# Library to cache the data
from functools import lru_cache

from .logger import Log

Log.info("***** Loading config.py")

# CET timezone (Europe/Madrid handles CET/CEST daylight saving)
CET_TZ = ZoneInfo('Europe/Madrid')


def now_cet():
    """Get current datetime in CET timezone"""
    return datetime.now(CET_TZ)


def now_cet_naive():
    """Get current local CET time as naive datetime for DB columns without timezone."""
    return now_cet().replace(tzinfo=None)


def today_cet():
    """Get current date in CET timezone"""
    return now_cet().date()


# Method to shorten a URL
def shorten_url(url: str) -> str:
    """ Shorten a URL """
    Log.debug(f"Shortening URL: {url}")
    try:
        """
        shortener = pyshorteners.Shortener()
        new_url = shortener.tinyurl.short(url)
        Log.debug(f"Shortened URL: {new_url}")
        """
        # TODO: Review how to obtain the new URL
        return url
    except Exception as e:
        Log.error("Error in shorten_url", err=e, sys=sys)
        return url

#######################################################################
# Config format for Flask apps, you create a class for each environment
#######################################################################


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __repr__(self) -> str:
        return "Config()"


# Valid SQLite URL forms are:
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # The path to the database file is relative to the project root.
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    development_database_url = os.getenv('DEVELOPMENT_DATABASE_URL', 'sqlite://database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir,
                     development_database_url.replace('sqlite://', ''))


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TESTING_DATABASE_URL", "sqlite:///:memory:")


class ProductionConfig(Config):
    PRODUCTION = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URL', '')

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    @classmethod
    def _warn_if_missing_db(cls):
        if not cls.SQLALCHEMY_DATABASE_URI:
            Log.warning(
                'PRODUCTION_DATABASE_URL is not set. '
                'Falling back to in-memory SQLite — ALL DATA WILL BE LOST on restart.')
            cls.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Settings(BaseSettings):
    # pydantic will automatically assume those default values if it doesn’t
    # find the corresponding environment variables.
    BASE_URL: str = "http://127.0.0.1:5000"
    LEVEL_LOG: str = os.getenv('LEVEL_LOG', "DEBUG, INFO, WARNING, ERROR")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-special-secret-key")
    CONFIG_MODE: str = os.getenv("CONFIG_MODE", "development")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_ENV = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    APP_DATA = {}

    class Config:
        # When you add the Config class with the path to your env_file to your
        # settings, pydantic loads your environment variables from the .env file.
        env_file = ".env"
        env_file_encoding = 'utf-8'

    def __init__(self) -> None:
        super().__init__()
        data_app = self.get_params_from_toml()
        app_data = data_app.get('tool', {}).get('falken_drinks', {}).get('app_data', {})
        Log.debug("Data from pyproject.toml:")
        Log.info_dict(data_app)
        self.APP_DATA = {
            'title': app_data.get('title', 'Falken Drinks'),
            'version': data_app['project']['version'],
            'author': data_app['project']['authors'][0]['name'],
            'license': data_app['project']['license'],
            'url_github': app_data.get('url_github', data_app['project']['urls']['Homepage']),
            'url_twitter': app_data.get('url_twitter', data_app['project']['urls']['Twitter']),
            'url_linkedin': app_data.get('url_linkedin', data_app['project']['urls']['LinkedIn']),
            'description': data_app['project']['description'],
            'copyright': app_data.get('copyright', ''),
            'features': app_data.get('features', []),
        }

    def get_params_from_toml(self) -> dict:
        """ Get the parameters from a TOML file """
        Log.info("Getting parameters from pyproject.toml")
        base_dir_toml = os.path.abspath(os.path.dirname(self.BASE_DIR))
        Log.debug(f"base_dir_toml: {base_dir_toml}")
        toml_file = os.path.join(base_dir_toml, "pyproject.toml")
        with open(toml_file, "r") as f:
            data = toml.load(f)
        return data


@lru_cache
def get_settings() -> Settings:
    Log.debug("Loading settings...")
    settings = Settings()
    return settings


def print_settings_environment(environment: dict) -> None:
    # Log.info_dict(f"Environment settings: {vars(environment)}")
    Log.info_dict(vars(environment), level_log="DEBUG")


@lru_cache
def print_app_config(app):
    """ Print the app config """
    Log.info("***** App Config:", style="red bold")

    # More complex way to print the app config instead Log.info_dict(dict(app.config))
    for key, value in app.config.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, type):
                    Log.info(
                        f"app.config: {key}: {k} -> {v.SQLALCHEMY_DATABASE_URI}")
                else:
                    Log.info(f"app.config: {key}: {k} -> {v}")
        else:
            Log.info(f"app.config: {key}: {value}")
