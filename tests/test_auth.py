# by Richi Rod AKA @richionline / falken20

import unittest

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
