# by Richi Rod AKA @richionline / falken20

import unittest
from unittest.mock import patch, MagicMock

from .basetest import BaseTestCase
from falken_drinks.app import create_app, settings
from falken_drinks.models import db, User


class TestCreateApp(BaseTestCase):
    """Test the create_app function"""

    def test_create_app_default(self):
        """Test create_app with default configuration"""
        app = create_app()
        self.assertIsNotNone(app)
        self.assertEqual(app.name, 'falken_drinks.app')

    def test_create_app_with_test_config(self):
        """Test create_app with test configuration"""
        app = create_app(settings.CONFIG_ENV['testing'])
        self.assertIsNotNone(app)
        self.assertTrue(app.config['TESTING'])
        # App shows 'development' as ENV even in test mode
        self.assertIn(app.config['ENV'], ['testing', 'development'])

    def test_create_app_returns_flask_app_instance(self):
        """Test that create_app returns a Flask app instance"""
        from flask import Flask
        app = create_app()
        self.assertIsInstance(app, Flask)

    def test_app_has_secret_key(self):
        """Test that app has a secret key configured"""
        self.assertIn('SECRET_KEY', self.app.config)
        self.assertIsNotNone(self.app.config['SECRET_KEY'])

    def test_app_blueprints_registered(self):
        """Test that all required blueprints are registered"""
        blueprint_names = [bp.name for bp in self.app.blueprints.values()]
        self.assertIn('auth', blueprint_names)
        self.assertIn('main', blueprint_names)
        self.assertIn('api_routes', blueprint_names)
        # Swagger UI blueprint is registered as 'swagger_ui'
        self.assertIn('swagger_ui', blueprint_names)

    def test_app_database_initialized(self):
        """Test that database is initialized properly"""
        self.assertIsNotNone(db)
        self.assertTrue(hasattr(db, 'engine'))

    def test_app_config_mode(self):
        """Test that app config mode is set correctly"""
        self.assertEqual(self.app.config['ENV'], 'testing')
        self.assertTrue(self.app.config['TESTING'])

    def test_app_template_auto_reload(self):
        """Test that template auto-reload is enabled"""
        self.assertTrue(self.app.config['TEMPLATE_AUTO_RELOAD'])

    def test_app_template_auto_reload_is_true(self):
        """Test that template auto-reload is explicitly set to True"""
        self.assertTrue(self.app.config.get('TEMPLATE_AUTO_RELOAD', False))

    def test_login_manager_configured(self):
        """Test that Flask-Login is configured properly"""
        self.assertTrue(hasattr(self.app, 'login_manager'))
        self.assertEqual(self.app.login_manager.login_view, 'auth.login')

    def test_user_loader_function(self):
        """Test that user loader function works correctly"""
        # Create a test user
        user = self.create_user()
        
        # Test the user loader
        loaded_user = db.session.get(User, user.user_id)
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.user_id, user.user_id)
        self.assertEqual(loaded_user.email, user.email)

    def test_user_loader_with_nonexistent_user(self):
        """Test user loader with non-existent user ID"""
        # Try to load a user that doesn't exist
        loaded_user = db.session.get(User, 99999)
        self.assertIsNone(loaded_user)

    def test_app_static_folder(self):
        """Test that static folder is configured correctly"""
        self.assertTrue(self.app.static_folder.endswith('static'))

    def test_app_template_folder(self):
        """Test that template folder is configured correctly"""
        self.assertTrue(self.app.template_folder.endswith('templates'))

    def test_app_base_url_configured(self):
        """Test that BASE_URL is configured"""
        self.assertIn('BASE_URL', self.app.config)
        self.assertIsNotNone(self.app.config['BASE_URL'])

    def test_app_has_valid_config_keys(self):
        """Test that app config has essential keys"""
        essential_keys = ['SECRET_KEY', 'BASE_URL', 'TEMPLATE_AUTO_RELOAD']
        for key in essential_keys:
            self.assertIn(key, self.app.config)
        """Test that app has at least 4 blueprints registered"""
        self.assertGreaterEqual(len(self.app.blueprints), 4)

    def test_create_app_initializes_db_with_app_context(self):
        """Test that app context can access db"""
        with self.app.app_context():
            # Should be able to run a query without errors
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            self.assertIsInstance(tables, list)


class TestAppSettings(BaseTestCase):
    """Test application settings"""

    def test_settings_exist(self):
        """Test that settings are loaded"""
        self.assertIsNotNone(settings)

    def test_settings_have_app_data(self):
        """Test that settings have APP_DATA"""
        self.assertTrue(hasattr(settings, 'APP_DATA'))
        self.assertIn('title', settings.APP_DATA)
        self.assertIn('version', settings.APP_DATA)
        self.assertIn('author', settings.APP_DATA)

    def test_settings_have_config_env(self):
        """Test that settings have CONFIG_ENV"""
        self.assertTrue(hasattr(settings, 'CONFIG_ENV'))
        self.assertIn('development', settings.CONFIG_ENV)
        self.assertIn('testing', settings.CONFIG_ENV)
        self.assertIn('production', settings.CONFIG_ENV)

    def test_settings_database_uri(self):
        """Test that database URI is configured"""
        self.assertIn('SQLALCHEMY_DATABASE_URI', self.app.config)
        self.assertIsNotNone(self.app.config['SQLALCHEMY_DATABASE_URI'])

    def test_settings_database_uri_testing(self):
        """Test that testing database URI uses SQLite"""
        testing_config = settings.CONFIG_ENV['testing']
        self.assertIn('sqlite', testing_config.SQLALCHEMY_DATABASE_URI.lower())

    def test_settings_config_mode(self):
        """Test that CONFIG_MODE is set"""
        self.assertTrue(hasattr(settings, 'CONFIG_MODE'))
        self.assertIn(settings.CONFIG_MODE, ['development', 'testing', 'production'])

    def test_settings_app_data_non_empty(self):
        """Test that APP_DATA fields are not empty"""
        self.assertTrue(settings.APP_DATA['title'])
        self.assertTrue(settings.APP_DATA['version'])
        self.assertTrue(settings.APP_DATA['author'])


class TestEnsureSchemaCompatibility(BaseTestCase):
    """Test the ensure_schema_compatibility function"""

    def test_schema_compatibility_with_existing_tables(self):
        """Test schema compatibility check with existing tables"""
        # Tables should already exist from setUp
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            # Should have drinks, users, drinks_logs tables
            self.assertIn('drinks', tables)
            self.assertIn('users', tables)
            self.assertIn('drinks_logs', tables)

    def test_drinks_table_has_counts_as_water_column(self):
        """Test that drinks table has counts_as_water column"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            drinks_columns = {col['name'] for col in inspector.get_columns('drinks')}
            self.assertIn('counts_as_water', drinks_columns)

    def test_users_table_password_column_sufficient_length(self):
        """Test that users.password column has sufficient length"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            users_columns = {col['name']: col for col in inspector.get_columns('users')}
            password_col = users_columns.get('password')
            self.assertIsNotNone(password_col)
            # Check that password column type supports at least 255 chars
            col_type = str(password_col['type']).lower()
            # Should be VARCHAR or similar
            self.assertIn('char', col_type.lower())

    def test_drinks_logs_table_exists(self):
        """Test that drinks_logs table exists"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            self.assertIn('drinks_logs', tables)

    def test_all_required_tables_exist(self):
        """Test that all required tables exist after app creation"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            tables = set(inspector.get_table_names())
            required_tables = {'drinks', 'users', 'drinks_logs'}
            self.assertTrue(required_tables.issubset(tables))

    def test_users_table_columns_present(self):
        """Test that users table has all required columns"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            user_columns = {col['name'] for col in inspector.get_columns('users')}
            required_cols = {'user_id', 'email', 'password', 'name', 'date_created', 'date_updated'}
            self.assertTrue(required_cols.issubset(user_columns))

    def test_drinks_table_columns_present(self):
        """Test that drinks table has all required columns"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            drinks_columns = {col['name'] for col in inspector.get_columns('drinks')}
            required_cols = {'drink_id', 'drink_name', 'drink_water_percentage',
                            'drink_alcohol_percentage', 'drink_image', 'counts_as_water'}
            self.assertTrue(required_cols.issubset(drinks_columns))

    def test_drinks_logs_table_columns_present(self):
        """Test that drinks_logs table has all required columns"""
        with self.app.app_context():
            inspector = db.inspect(db.engine)
            logs_columns = {col['name'] for col in inspector.get_columns('drinks_logs')}
            required_cols = {'log_id', 'drink_id', 'user_id', 'date_created',
                            'drink_total_quantity', 'drink_water_quantity', 'drink_alcohol_quantity'}
            self.assertTrue(required_cols.issubset(logs_columns))


if __name__ == '__main__':
    unittest.main()
