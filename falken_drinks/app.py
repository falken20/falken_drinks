# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
import os
import sys
from dotenv import load_dotenv, find_dotenv
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

from .logger import Log, console
from .config import get_settings, print_settings_environment
from .cache import check_cache
from .models import db, init_db_if_needed

Log.info("***** Loading app.py")

# Set environment vars
load_dotenv(find_dotenv())

settings = get_settings()
Log.info("***** Environment vars:")
_safe_settings = {k: ('***' if k.upper() in ('SECRET_KEY', 'PASSWORD', 'TOKEN') else v)
                  for k, v in settings.dict().items()}
Log.info_dict(_safe_settings, level_log="INFO")

console.rule(settings.APP_DATA['title'] + " "
             + " " + settings.APP_DATA['version'] + " " + settings.APP_DATA['author'])

# Cache info
check_cache()

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _migrate_drinks_counts_as_water(inspector, dialect):
    """Migrate drinks.counts_as_water column if missing."""
    if 'drinks' not in inspector.get_table_names():
        return
    drinks_columns = {column['name'] for column in inspector.get_columns('drinks')}
    if 'counts_as_water' in drinks_columns:
        return
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


def _migrate_users_password_length(inspector, dialect):
    """Migrate users.password to max length 255 if shorter."""
    if 'users' not in inspector.get_table_names() or dialect != 'postgresql':
        return
    users_columns = {column['name']: column for column in inspector.get_columns('users')}
    password_column = users_columns.get('password')
    current_length = getattr(password_column['type'], 'length', None) if password_column else None
    if current_length is None or current_length >= 255:
        return
    Log.warning('Column users.password shorter than 255. Applying automatic migration...')
    with db.engine.begin() as conn:
        conn.execute(db.text('ALTER TABLE users ALTER COLUMN password TYPE VARCHAR(255)'))
    Log.info('Automatic migration applied for users.password length')


def _migrate_drink_logs_date_created(inspector, dialect):
    """Migrate drinks_logs.date_created from DATE to TIMESTAMP if needed."""
    if 'drinks_logs' not in inspector.get_table_names() or dialect != 'postgresql':
        return
    drinks_log_columns = {
        column['name']: column for column in inspector.get_columns('drinks_logs')
    }
    date_created_column = drinks_log_columns.get('date_created')
    if not date_created_column:
        return
    column_type = str(date_created_column['type']).lower()
    if 'date' not in column_type or 'timestamp' in column_type:
        return
    msg = 'Column drinks_logs.date_created is DATE. Applying automatic migration to TIMESTAMP...'
    Log.warning(msg)
    with db.engine.begin() as conn:
        conn.execute(db.text(
            'ALTER TABLE drinks_logs ALTER COLUMN date_created TYPE TIMESTAMP '
            'USING date_created::timestamp'
        ))
    Log.info('Automatic migration applied for drinks_logs.date_created type')


def _migrate_drinks_user_id(inspector):
    """Migrate drinks.user_id column if missing."""
    if 'drinks' not in inspector.get_table_names():
        return
    drinks_columns = {column['name'] for column in inspector.get_columns('drinks')}
    if 'user_id' in drinks_columns:
        return
    Log.warning("Column drinks.user_id missing. Applying automatic migration...")
    with db.engine.begin() as conn:
        conn.execute(db.text(
            'ALTER TABLE drinks ADD COLUMN user_id INTEGER REFERENCES users(user_id)'
        ))
    Log.info('Automatic migration applied for drinks.user_id')


def _migrate_users_name_nullable(inspector, dialect):
    """Migrate users.name to nullable if NOT NULL."""
    if 'users' not in inspector.get_table_names() or dialect != 'postgresql':
        return
    users_columns = {column['name']: column for column in inspector.get_columns('users')}
    name_column = users_columns.get('name')
    if not name_column or name_column.get('nullable', True):
        return
    msg = "Column users.name is NOT NULL. Applying automatic migration to nullable..."
    Log.warning(msg)
    with db.engine.begin() as conn:
        conn.execute(db.text('ALTER TABLE users ALTER COLUMN name DROP NOT NULL'))
    Log.info('Automatic migration applied for users.name nullable')


def ensure_schema_compatibility(app):
    """Apply minimal backward-compatible schema updates when old DBs are detected."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        dialect = db.engine.dialect.name
        _migrate_drinks_counts_as_water(inspector, dialect)
        _migrate_users_password_length(inspector, dialect)
        _migrate_drink_logs_date_created(inspector, dialect)
        _migrate_drinks_user_id(inspector)
        _migrate_users_name_nullable(inspector, dialect)


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
            if config_mode == 'production' and not os.getenv('PRODUCTION_DATABASE_URL'):
                Log.warning(
                    'PRODUCTION_DATABASE_URL is not set. '
                    'Falling back to in-memory SQLite — ALL DATA WILL BE LOST on restart.')
        app.config['TEMPLATE_AUTO_RELOAD'] = True
        app.config['DEBUG'] = config_mode == 'development'
        app.config['ENV'] = config_mode
        app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB max request size
        app.config['REMEMBER_COOKIE_HTTPONLY'] = True
        app.config['REMEMBER_COOKIE_SECURE'] = config_mode == 'production'
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SECURE'] = config_mode == 'production'
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        Log.info(f"App config loaded from {config_mode} successfully")

        # CSRF protection for all forms
        CSRFProtect(app)

        # Rate limiter (in-memory storage; switch to Redis in production)
        Limiter(
            get_remote_address,
            app=app,
            default_limits=[],
            storage_uri='memory://'
        )

        # HTTP security headers (CSP relaxed to allow CDN assets)
        csp = {
            'default-src': ["'self'"],
            'script-src': [
                "'self'",
                'https://cdn.jsdelivr.net',
                'https://cdnjs.cloudflare.com',
            ],
            'style-src': [
                "'self'",
                "'unsafe-inline'",
                'https://cdn.jsdelivr.net',
                'https://cdnjs.cloudflare.com',
            ],
            'img-src': ["'self'", 'data:'],
            'font-src': ["'self'", 'https://cdn.jsdelivr.net'],
        }
        Talisman(
            app,
            force_https=config_mode == 'production',
            strict_transport_security=config_mode == 'production',
            content_security_policy=csp,
            frame_options='DENY',
            x_content_type_options=True,
            referrer_policy='strict-origin-when-cross-origin',
        )

        db.init_app(app)
        Log.info("Database initialized successfully")

        # Auto-create tables in development/testing if they don't exist
        if config_mode in ['development', 'testing'] or test_config is not None:
            init_db_if_needed(app)

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
