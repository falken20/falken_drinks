import unittest

from . import basetest


class TestMain(basetest.BaseTestCase):

    def test_index(self):
        # First we need to create a user and login
        """
        response = self.client.post(
            '/signup', data=self.mock_user, follow_redirects=True)
        response = self.client.post(
            '/login', data=self.mock_user, follow_redirects=True)
        """
        self.create_user()
        self.login_http(self)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_show_grouped(self):
        # First we need to create a user and login
        self.create_user()
        self.login_http(self)

        response = self.client.get('/show_grouped/')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_list_group.html', response.data)

    def test_profile(self):
        # First we need to create a user and login
        self.create_user()
        self.login_http(self)

        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
