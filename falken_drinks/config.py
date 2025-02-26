# by Richi Rod AKA @richionline / falken20
# ./falken_plants/config.py

# Library that uses type annotation to validate data and manage settings.
# from pydantic import BaseSettings # Old version
import os
import sys
from pydantic.v1 import BaseSettings
# from pydantic_settings import BaseSettings # New version
# import pyshorteners

# Library to cache the data
from functools import lru_cache

from .logger import Log

print("Loading config.py")

__title__ = 'Falken Plants'
__version__ = '1.0.0'
__author__ = 'Falken'
__url_github__ = 'https://github.com/falken20/'
__url_twitter__ = 'https://twitter.com/richionline'
__url_linkedin__ = 'https://www.linkedin.com/in/richionline/'
__license__ = 'MIT License'
__copyright__ = '© 2024 by Richi Rod AKA @richionline / falken20'
__features__ = [
]


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
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.SQLALCHEMY_DATABASE_URI

    def __repr__(self) -> str:
        return "Config()"

    def __str__(self) -> str:
        return self.SQLALCHEMY_DATABASE_URI


# Valid SQLite URL forms are:
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # The path to the database file is relative to the project root.
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir,
                     os.getenv("DEVELOPMENT_DATABASE_URL").replace("sqlite://", ""))


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TESTING_DATABASE_URL", "sqlite:///:memory:")


class ProductionConfig(Config):
    PRODUCTION = True
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ['PRODUCTION_DATABASE_URL'].replace("://", "ql://", 1)
    # URL from Neon is not neccesary change :// by ql://
    SQLALCHEMY_DATABASE_URI = os.environ['PRODUCTION_DATABASE_URL']


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
    APP_DATA = {
        'title': __title__,
        'version': __version__,
        'author': __author__,
        'url_github': __url_github__,
        'url_twitter': __url_twitter__,
        'url_linkedin': __url_linkedin__,
        'license': __license__,
        'copyrigth': __copyright__,
        'features': __features__,
    }

    class Config:
        # When you add the Config class with the path to your env_file to your
        # settings, pydantic loads your environment variables from the .env file.
        env_file = ".env"
        env_file_encoding = 'utf-8'


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
