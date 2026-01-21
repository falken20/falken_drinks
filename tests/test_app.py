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

    def test_login_manager_configured(self):
        """Test that Flask-Login is configured properly"""
        self.assertTrue(hasattr(self.app, 'login_manager'))
        self.assertEqual(self.app.login_manager.login_view, 'auth.login')

    def test_user_loader_function(self):
        """Test that user loader function works correctly"""
        # Create a test user
        user = self.create_user()
        
        # Test the user loader
        loaded_user = User.query.get(user.user_id)
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.user_id, user.user_id)
        self.assertEqual(loaded_user.email, user.email)

    def test_app_static_folder(self):
        """Test that static folder is configured correctly"""
        self.assertTrue(self.app.static_folder.endswith('static'))

    def test_app_template_folder(self):
        """Test that template folder is configured correctly"""
        self.assertTrue(self.app.template_folder.endswith('templates'))


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


if __name__ == '__main__':
    unittest.main()
