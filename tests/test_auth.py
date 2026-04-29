# by Richi Rod AKA @richionline / falken20

import unittest
from unittest.mock import patch

from . import basetest

class TestAuth(basetest.BaseTestCase):
    def test_auth_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_auth_login_post(self):
        response = self.client.post('/login', data=self.mock_user, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_auth_login_post_error(self):
        response = self.client.post('/login', data=self.mock_user_unknown, follow_redirects=True)
        self.assertIn('Please check your login details and try again.', response.text)
        self.assertEqual(response.status_code, 200)
    
    def test_auth_signup(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_auth_signup_post_user_exists(self):
        response = self.client.post('/signup', data=self.mock_user, follow_redirects=True)
        response = self.client.post('/signup', data=self.mock_user, follow_redirects=True)
        self.assertIn('Email address already exists.', response.text)
        self.assertEqual(response.status_code, 200)

    @patch('falken_drinks.auth.db.session.commit', side_effect=Exception('Database unavailable'))
    def test_auth_signup_post_shows_error_to_user(self, _commit_mock):
        response = self.client.post('/signup', data=self.mock_user, follow_redirects=True)
        # Generic error message shown (no internal details leaked)
        self.assertIn('Error creating your account. Please try again.', response.text)
        self.assertNotIn('Database unavailable', response.text)
        self.assertEqual(response.status_code, 200)

    def test_auth_logout(self):
        self.create_user()
        self.login_http(self)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_auth_logout_rediret_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn('Please log in to access this page.', response.text)
        self.assertEqual(response.status_code, 200)

    def test_auth_signup_post_user_new(self):
        response = self.client.post('/signup', data=self.mock_user, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # ----- Security validations added in the hardening audit -----

    def test_auth_login_invalid_email_format(self):
        """Login with a malformed email must show the generic error and not hit the DB."""
        response = self.client.post(
            '/login',
            data={'email': 'not-an-email', 'password': 'password'},
            follow_redirects=True,
        )
        self.assertIn('Please check your login details and try again.', response.text)
        self.assertEqual(response.status_code, 200)

    def test_auth_signup_invalid_email_format(self):
        response = self.client.post(
            '/signup',
            data={'email': 'bademail', 'name': 'x', 'password': 'password123'},
            follow_redirects=True,
        )
        self.assertIn('Please enter a valid email address.', response.text)
        self.assertEqual(response.status_code, 200)

    def test_auth_signup_password_too_short(self):
        response = self.client.post(
            '/signup',
            data={'email': 'ok@mail.com', 'name': 'x', 'password': 'short'},
            follow_redirects=True,
        )
        self.assertIn('Password must be at least 8 characters long.', response.text)
        self.assertEqual(response.status_code, 200)

    def test_auth_logout_redirects_to_login_not_signup(self):
        """Regression: logout must redirect to /login, not /signup."""
        self.create_user()
        self.login_http(self)
        response = self.client.get('/logout', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/login'))
