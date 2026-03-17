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


def ensure_schema_compatibility(app):
    """Apply minimal backward-compatible schema updates when old DBs are detected."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        table_names = set(inspector.get_table_names())
        dialect = db.engine.dialect.name

        if 'drinks' in table_names:
            drinks_columns = {column['name'] for column in inspector.get_columns('drinks')}
            if 'counts_as_water' not in drinks_columns:
                Log.warning("Column drinks.counts_as_water missing. Applying automatic migration...")
                with db.engine.begin() as conn:
                    if dialect == 'postgresql':
                        conn.execute(db.text(
                            'ALTER TABLE drinks ADD COLUMN counts_as_water BOOLEAN NOT NULL DEFAULT TRUE'
                        ))
                        conn.execute(db.text(
                            'UPDATE drinks SET counts_as_water = FALSE WHERE drink_alcohol_percentage > 0'
                        ))
                    else:
                        conn.execute(db.text(
                            'ALTER TABLE drinks ADD COLUMN counts_as_water BOOLEAN NOT NULL DEFAULT 1'
                        ))
                        conn.execute(db.text(
                            'UPDATE drinks SET counts_as_water = 0 WHERE drink_alcohol_percentage > 0'
                        ))
                Log.info('Automatic migration applied for drinks.counts_as_water')

        if 'users' in table_names:
            users_columns = {column['name']: column for column in inspector.get_columns('users')}
            password_column = users_columns.get('password')
            current_length = getattr(password_column['type'], 'length', None) if password_column else None

            if current_length is not None and current_length < 255 and dialect == 'postgresql':
                Log.warning('Column users.password shorter than 255. Applying automatic migration...')
                with db.engine.begin() as conn:
                    conn.execute(db.text('ALTER TABLE users ALTER COLUMN password TYPE VARCHAR(255)'))
                Log.info('Automatic migration applied for users.password length')


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

        ensure_schema_compatibility(app)
        Log.info('Database schema compatibility check completed')

        # A user loader tells Flask-Login how to find a specific user from the ID that is stored in their
        # session cookie.
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            try:
                # SQLAlchemy 2.x: use Session.get instead of legacy Query.get
                return db.session.get(User, int(user_id))
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
