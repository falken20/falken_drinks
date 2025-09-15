# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
import os
import sys
from dotenv import load_dotenv, find_dotenv
from flask_login import LoginManager

from .logger import Log, console
from .config import get_settings, print_settings_environment
from .cache import check_cache
from .models import db

Log.info("***** Loading app.py")

# Set environment vars
load_dotenv(find_dotenv())

settings = get_settings()
Log.info("***** Environment vars:")
Log.info_dict(settings.dict(), level_log="INFO")

console.rule(settings.APP_DATA['title'] + " " 
             + " " + settings.APP_DATA['version'] + " " + settings.APP_DATA['author'])

# Cache info
check_cache()

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(test_config=None):
    try:
        Log.info("***** Creating app...")

        config_mode = settings.CONFIG_MODE
        Log.info(f"***** Running in {config_mode.upper()} mode")

        app = Flask(__name__, template_folder="../templates",
                    static_folder="../static")
        Log.debug(f"App name: {app.name}")
        app.config.from_object(settings)

        # If we are executing tests, we will use the test configuration
        if test_config is not None:
            app.config.from_object(test_config)
        else:
            app.config.from_object(settings.CONFIG_ENV[config_mode])
        app.config['TEMPLATE_AUTO_RELOAD'] = True
        app.config['DEBUG'] = True if config_mode == "development" else False
        app.config['ENV'] = config_mode
        Log.info(f"App config loaded from {config_mode} successfully")

        db.init_app(app)
        Log.info("Database initialized successfully")

        # A user loader tells Flask-Login how to find a specific user from the ID that is stored in their
        # session cookie.
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            try:
                # Since the user_id is just the primary key of our user table, use it in the query for the user
                return User.query.get(int(user_id))
            except Exception:
                Log.error("Error loading user", None, sys)
                return None
        Log.info("Login manager initialized successfully")

        # blueprint for auth routes in our app
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        Log.info("Auth blueprint registered successfully")

        # blueprint for non-auth parts of app
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        Log.info("Main blueprint registered successfully")

        # Blueprint for routes
        from .routes import api_routes as routes_blueprint
        app.register_blueprint(routes_blueprint)
        Log.info("Routes blueprint registered successfully")

        # blueprint for swagger
        from .swagger import swagger_ui_blueprint, SWAGGER_URL
        app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
        Log.debug(f"Running Swagger in {SWAGGER_URL}")

        if config_mode == "testing" or test_config is not None:
            Log.info("***** App config TESTING mode:")
            print_settings_environment(settings.CONFIG_ENV["testing"])
        else:
            # print_app_config(app)
            Log.info("***** App config:")
            Log.info_dict(dict(app.config), level_log="INFO")

        Log.info(f"APP URL: {app.config['BASE_URL']}")
        Log.info(f"APP version: {settings.APP_DATA['version']}")
        Log.info(f"APP Environment: {app.config['CONFIG_MODE']}")
        Log.info("***** App created succesfully")

        return app

    except Exception as err:
        Log.error("Error creating app", err, sys)
        return None


# If FLASK_DEBUG is True, the reloader will be enabled by default and the thread starts twice.
if __name__ == '__main__':
    Log.info("Initializing app...", style="red bold")
    app = create_app()
