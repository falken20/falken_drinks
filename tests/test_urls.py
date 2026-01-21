import unittest
import pytest

from . import basetest
from falken_drinks.controllers import ControllerDrinks


class TestUrls(basetest.BaseTestCase):

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_list_create_plants(self):
        # First we need to create a user and login
        self.create_user()
        self.login_http(self)

        response = self.client.get('/plants')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_list.html', response.data)
        response = self.client.put('/plants')
        self.assertEqual(response.status_code, 405)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_list_create_plants_hidden_post(self):
        self.create_user()
        self.login_http(self)
        # POST with _method=POST
        response = self.client.post('/plants', data=self.MOCK_PLANT)
        self.assertEqual(response.status_code, 302)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_list_create_plants_hidden_put(self):
        self.create_user()
        self.login_http(self)
        # POST with _method=PUT
        mock_plant = self.MOCK_PLANT
        mock_plant['_method'] = 'PUT'
        response = self.client.post('/plants', data=mock_plant)
        self.assertEqual(response.status_code, 302)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_list_create_plants_post(self):
        self.create_user()
        self.login_http(self)
        # response = self.client.post('/plants', data={'name': 'Test Plant', '_method': 'POST'})
        response = self.client.post('/plants', data=self.MOCK_PLANT)
        # Assuming redirect after post
        self.assertEqual(response.status_code, 302)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_get_update_delete_plants_get(self):
        user = self.create_user()
        self.login_http(self)
        response = self.client.get('/plants/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_form.html', response.data)

        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        response = self.client.delete(f'/plants/{plant.id}')
        self.assertEqual(response.status_code, 200)

        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        response = self.client.put(f'/plants/{plant.id}', data=self.MOCK_PLANT)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_view_create_plant(self):
        self.create_user()
        self.login_http(self)
        response = self.client.get('/plants/create')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_form.html', response.data)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_view_update_plant(self):
        self.create_user()
        self.login_http(self)
        response = self.client.get('/plants/update/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_form.html', response.data)

    @pytest.mark.skip(reason="Plant management feature has been removed")
    def test_delete_plant(self):
        user = self.create_user()
        self.login_http(self)
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        response = self.client.get(f'/plants/{plant.id}/delete')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
