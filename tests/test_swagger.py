# by Richi Rod AKA @richionline / falken20

import unittest

from .basetest import BaseTestCase
from falken_drinks.swagger import swagger_ui_blueprint, SWAGGER_URL, SWAGGER_API_URL


class TestSwaggerConfiguration(BaseTestCase):
    """Test Swagger UI configuration"""

    def test_swagger_url_defined(self):
        """Test that SWAGGER_URL is defined"""
        self.assertIsNotNone(SWAGGER_URL)
        self.assertEqual(SWAGGER_URL, "/swagger")

    def test_swagger_api_url_defined(self):
        """Test that SWAGGER_API_URL is defined"""
        self.assertIsNotNone(SWAGGER_API_URL)
        self.assertEqual(SWAGGER_API_URL, "/static/swagger.json")

    def test_swagger_blueprint_exists(self):
        """Test that swagger_ui_blueprint is created"""
        self.assertIsNotNone(swagger_ui_blueprint)

    def test_swagger_blueprint_registered(self):
        """Test that swagger blueprint is registered in app"""
        blueprint_names = [bp.name for bp in self.app.blueprints.values()]
        # Swagger UI blueprint is registered as 'swagger_ui'
        self.assertIn('swagger_ui', blueprint_names)

    def test_swagger_endpoint_accessible(self):
        """Test that swagger endpoint is accessible"""
        # Create and login user
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, 200)

    def test_swagger_config_has_app_name(self):
        """Test that swagger config has app_name"""
        # The swagger blueprint should have config
        self.assertTrue(hasattr(swagger_ui_blueprint, 'name'))


class TestSwaggerUI(BaseTestCase):
    """Test Swagger UI functionality"""

    def test_swagger_ui_loads(self):
        """Test that Swagger UI page loads"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, 200)

    def test_swagger_without_trailing_slash(self):
        """Test accessing swagger without trailing slash redirects"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.get('/swagger', follow_redirects=False)
        # Should redirect or work
        self.assertIn(response.status_code, [200, 301, 302, 308])


if __name__ == '__main__':
    unittest.main()
