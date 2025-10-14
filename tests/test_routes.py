# by Richi Rod AKA @richionline / falken20

import json
from datetime import date

from .basetest import BaseTestCase
from falken_drinks.models import db, User, Drink, DrinkLog


class TestAddDrinkRoute(BaseTestCase):
    """Test /api/add_drink endpoint"""

    def test_add_drink_success(self):
        """Test adding a drink log successfully"""
        # Create and login user
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Add drink
        response = self.client.post('/api/add_drink',
                                   data=json.dumps(self.MOCK_DRINK_LOG),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('Added', data['message'])

    def test_add_drink_unauthorized(self):
        """Test adding drink without login"""
        response = self.client.post('/api/add_drink',
                                   data=json.dumps(self.MOCK_DRINK_LOG),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 401)

    def test_add_drink_no_data(self):
        """Test adding drink with no data"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.post('/api/add_drink',
                                   data=json.dumps({}),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_add_drink_invalid_amount(self):
        """Test adding drink with invalid amount"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        invalid_data = {'drink_name': 'Water', 'amount': 0, 'alcohol_percentage': 0}
        response = self.client.post('/api/add_drink',
                                   data=json.dumps(invalid_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_add_drink_invalid_data_types(self):
        """Test adding drink with invalid data types"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        invalid_data = {'drink_name': 'Water', 'amount': 'invalid', 'alcohol_percentage': 0}
        response = self.client.post('/api/add_drink',
                                   data=json.dumps(invalid_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


class TestGetDrinksRoute(BaseTestCase):
    """Test /api/drinks GET endpoint"""

    def test_get_drinks_success(self):
        """Test getting all drinks"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Create a test drink
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        response = self.client.get('/api/drinks')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('drinks', data)
        self.assertGreater(len(data['drinks']), 0)

    def test_get_drinks_unauthorized(self):
        """Test getting drinks without login"""
        response = self.client.get('/api/drinks')
        self.assertEqual(response.status_code, 401)

    def test_get_drinks_empty(self):
        """Test getting drinks when none exist"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.get('/api/drinks')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['drinks']), 0)


class TestCreateDrinkRoute(BaseTestCase):
    """Test /api/drinks POST endpoint"""

    def test_create_drink_success(self):
        """Test creating a new drink"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.post('/api/drinks',
                                   data=json.dumps(self.MOCK_DRINK),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('created successfully', data['message'])

    def test_create_drink_unauthorized(self):
        """Test creating drink without login"""
        response = self.client.post('/api/drinks',
                                   data=json.dumps(self.MOCK_DRINK),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 401)

    def test_create_drink_no_name(self):
        """Test creating drink without name"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        invalid_data = {'drink_name': '', 'drink_water_percentage': 100, 'drink_alcohol_percentage': 0}
        response = self.client.post('/api/drinks',
                                   data=json.dumps(invalid_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_create_drink_invalid_percentages(self):
        """Test creating drink with invalid percentages"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        invalid_data = {'drink_name': 'Test', 'drink_water_percentage': 60, 'drink_alcohol_percentage': 50}
        response = self.client.post('/api/drinks',
                                   data=json.dumps(invalid_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('cannot exceed 100%', data['message'])

    def test_create_drink_duplicate_name(self):
        """Test creating drink with existing name"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Create first drink
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        # Try to create duplicate
        duplicate_data = {'drink_name': 'Test Water', 'drink_water_percentage': 100, 'drink_alcohol_percentage': 0}
        response = self.client.post('/api/drinks',
                                   data=json.dumps(duplicate_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


class TestUpdateDrinkRoute(BaseTestCase):
    """Test /api/drinks/<id> PUT endpoint"""

    def test_update_drink_success(self):
        """Test updating a drink"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Create a drink
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        # Update it
        update_data = {'drink_name': 'Updated Water', 'drink_water_percentage': 90, 'drink_alcohol_percentage': 0}
        response = self.client.put(f'/api/drinks/{drink.drink_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('updated successfully', data['message'])

    def test_update_drink_not_found(self):
        """Test updating non-existent drink"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        update_data = {'drink_name': 'Test', 'drink_water_percentage': 100, 'drink_alcohol_percentage': 0}
        response = self.client.put('/api/drinks/999',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_update_drink_unauthorized(self):
        """Test updating drink without login"""
        response = self.client.put('/api/drinks/1',
                                   data=json.dumps(self.MOCK_DRINK),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 401)


class TestDeleteDrinkRoute(BaseTestCase):
    """Test /api/drinks/<id> DELETE endpoint"""

    def test_delete_drink_success(self):
        """Test deleting a drink"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Create a drink
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        response = self.client.delete(f'/api/drinks/{drink.drink_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('deleted successfully', data['message'])

    def test_delete_drink_not_found(self):
        """Test deleting non-existent drink"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.delete('/api/drinks/999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_delete_drink_with_logs(self):
        """Test deleting drink that has logs"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Create drink and log
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0)
        db.session.add(drink_log)
        db.session.commit()
        
        response = self.client.delete(f'/api/drinks/{drink.drink_id}')
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('Cannot delete', data['message'])

    def test_delete_drink_unauthorized(self):
        """Test deleting drink without login"""
        response = self.client.delete('/api/drinks/1')
        self.assertEqual(response.status_code, 401)


class TestDeleteDrinkLogRoute(BaseTestCase):
    """Test /api/delete_drink_log/<id> DELETE endpoint"""

    def test_delete_drink_log_success(self):
        """Test deleting a drink log"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        # Create drink and log
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0)
        db.session.add(drink_log)
        db.session.commit()
        
        response = self.client.delete(f'/api/delete_drink_log/{drink_log.log_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_delete_drink_log_not_found(self):
        """Test deleting non-existent drink log"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.delete('/api/delete_drink_log/999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_delete_drink_log_unauthorized(self):
        """Test deleting drink log without login"""
        response = self.client.delete('/api/delete_drink_log/1')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    import unittest
    unittest.main()
