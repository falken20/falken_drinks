# by Richi Rod AKA @richionline / falken20

import json
from datetime import date
from datetime import date
from unittest.mock import patch

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
        
        # Flask-Login redirects to login page (302) instead of returning 401
        self.assertEqual(response.status_code, 302)

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
        
        # Server returns 500 for type conversion errors
        self.assertIn(response.status_code, [400, 500])
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_add_drink_with_custom_time(self):
        """Test adding a drink log with explicit HH:MM time"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        drink_data = {
            'drink_name': 'Water',
            'amount': 250,
            'alcohol_percentage': 0,
            'drink_time': '13:45'
        }
        response = self.client.post(
            '/api/add_drink',
            data=json.dumps(drink_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.data)
        self.assertTrue(payload['success'])

        log = DrinkLog.query.filter_by(user_id=user.user_id).order_by(DrinkLog.log_id.desc()).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.date_created.hour, 13)
        self.assertEqual(log.date_created.minute, 45)
        self.assertEqual(log.date_created.date(), date.today())

    def test_add_drink_failed_get_or_create(self):
        """Test add_drink returns 500 when drink cannot be created/found"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        payload = {'drink_name': 'Water', 'amount': 250, 'alcohol_percentage': 0}
        with patch('falken_drinks.routes.ControllerDrinks.get_or_create_drink', return_value=None):
            response = self.client.post('/api/add_drink',
                                        data=json.dumps(payload),
                                        content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_add_drink_failed_save_log(self):
        """Test add_drink returns 500 when drink log cannot be saved"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        payload = {'drink_name': 'Water', 'amount': 250, 'alcohol_percentage': 0}
        with patch('falken_drinks.routes.ControllerDrinkLogs.add_drink_log', return_value=None):
            response = self.client.post('/api/add_drink',
                                        data=json.dumps(payload),
                                        content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_add_drink_unhandled_exception(self):
        """Test add_drink handles unexpected exceptions"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        payload = {'drink_name': 'Water', 'amount': 250, 'alcohol_percentage': 0}
        with patch('falken_drinks.routes.ControllerDrinks.get_or_create_drink', side_effect=Exception('boom')):
            response = self.client.post('/api/add_drink',
                                        data=json.dumps(payload),
                                        content_type='application/json')

        self.assertEqual(response.status_code, 500)
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
        # Flask-Login redirects to login page (302) instead of returning 401
        self.assertEqual(response.status_code, 302)

    def test_get_drinks_empty(self):
        """Test getting drinks when none exist"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)
        
        response = self.client.get('/api/drinks')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['drinks']), 0)

    def test_get_drinks_unhandled_exception(self):
        """Test get_drinks handles unexpected exceptions"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        with patch('falken_drinks.routes.ControllerDrinks.get_drinks', side_effect=Exception('boom')):
            response = self.client.get('/api/drinks')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


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
        
        # Flask-Login redirects to login page (302) instead of returning 401
        self.assertEqual(response.status_code, 302)

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

    def test_create_drink_no_data(self):
        """Test creating drink with no data body"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        response = self.client.post('/api/drinks', data='null', content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_create_drink_invalid_percentage_type(self):
        """Test creating drink with non-numeric percentages"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        invalid_data = {
            'drink_name': 'Invalid',
            'drink_water_percentage': 'abc',
            'drink_alcohol_percentage': 0
        }
        response = self.client.post('/api/drinks',
                                    data=json.dumps(invalid_data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_create_drink_failed_save(self):
        """Test creating drink returns 500 when repository save fails"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        with patch('falken_drinks.routes.ControllerDrinks.add_drink', return_value=None):
            response = self.client.post('/api/drinks',
                                        data=json.dumps(self.MOCK_DRINK),
                                        content_type='application/json')

        self.assertEqual(response.status_code, 500)
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
        
        # Flask-Login redirects to login page (302) instead of returning 401
        self.assertEqual(response.status_code, 302)

    def test_update_drink_invalid_percentages(self):
        """Test updating drink with percentages that exceed 100%"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()

        invalid_data = {'drink_name': 'Test', 'drink_water_percentage': 70, 'drink_alcohol_percentage': 60}
        response = self.client.put(f'/api/drinks/{drink.drink_id}',
                                   data=json.dumps(invalid_data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('cannot exceed 100%', data['message'])

    def test_update_drink_duplicate_name(self):
        """Test updating drink to a name that already exists in another drink"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        drink1 = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        drink2 = Drink(drink_name='Coffee', drink_water_percentage=98, drink_alcohol_percentage=0)
        db.session.add_all([drink1, drink2])
        db.session.commit()

        # Try to rename drink2 to an existing name
        update_data = {'drink_name': 'Water', 'drink_water_percentage': 98, 'drink_alcohol_percentage': 0}
        response = self.client.put(f'/api/drinks/{drink2.drink_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_update_drink_no_data(self):
        """Test updating drink without sending any data body"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()

        # Send explicit JSON null so Flask's get_json() returns None → 400
        response = self.client.put(f'/api/drinks/{drink.drink_id}',
                                   data='null',
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_update_drink_counts_as_water_false(self):
        """Test updating drink with counts_as_water=False (alcoholic drink)"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        drink = Drink(drink_name='Beer', drink_water_percentage=95, drink_alcohol_percentage=5)
        db.session.add(drink)
        db.session.commit()

        update_data = {
            'drink_name': 'Beer Updated',
            'drink_water_percentage': 93,
            'drink_alcohol_percentage': 7,
            'counts_as_water': False
        }
        response = self.client.put(f'/api/drinks/{drink.drink_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertFalse(data['drink']['counts_as_water'])

    def test_update_drink_invalid_percentage_type(self):
        """Test updating drink with non-numeric percentages"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        drink = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()

        invalid_data = {'drink_name': 'Water', 'drink_water_percentage': 'abc', 'drink_alcohol_percentage': 0}
        response = self.client.put(f'/api/drinks/{drink.drink_id}',
                                   data=json.dumps(invalid_data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_update_drink_unhandled_exception(self):
        """Test update_drink handles unexpected exceptions and returns 500"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        with patch('falken_drinks.routes.ControllerDrinks.get_drink', side_effect=Exception('boom')):
            response = self.client.put('/api/drinks/1',
                                       data=json.dumps({'drink_name': 'Any'}),
                                       content_type='application/json')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


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
        # Flask-Login redirects to login page (302) instead of returning 401
        self.assertEqual(response.status_code, 302)

    def test_delete_drink_unhandled_exception(self):
        """Test delete_drink handles unexpected exceptions"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        with patch('falken_drinks.routes.ControllerDrinks.get_drink', side_effect=Exception('boom')):
            response = self.client.delete('/api/drinks/1')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


class TestCreateDrinkCountsAsWaterRoute(BaseTestCase):
    """Test counts_as_water field behavior in drink creation"""

    def test_create_drink_counts_as_water_explicit_false(self):
        """Test creating an alcoholic drink with counts_as_water=False"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        data = {
            'drink_name': 'Beer',
            'drink_water_percentage': 95,
            'drink_alcohol_percentage': 5,
            'counts_as_water': False
        }
        response = self.client.post('/api/drinks',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertTrue(result['success'])
        self.assertFalse(result['drink']['counts_as_water'])

    def test_create_drink_counts_as_water_default_true(self):
        """Test creating a non-alcoholic drink defaults counts_as_water to True"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        data = {
            'drink_name': 'Herbal Tea',
            'drink_water_percentage': 99,
            'drink_alcohol_percentage': 0
        }
        response = self.client.post('/api/drinks',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertTrue(result['success'])
        self.assertTrue(result['drink']['counts_as_water'])

    def test_create_drink_out_of_range_percentage(self):
        """Test creating drink with a single percentage > 100"""
        user = self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        data = {
            'drink_name': 'Invalid Drink',
            'drink_water_percentage': 150,
            'drink_alcohol_percentage': 0
        }
        response = self.client.post('/api/drinks',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertFalse(result['success'])


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
        # Flask-Login redirects to login page (302) instead of returning 401
        self.assertEqual(response.status_code, 302)

    def test_delete_drink_log_unhandled_exception(self):
        """Test delete_drink_log handles unexpected exceptions"""
        self.create_user()
        self.client.post('/login', data=self.mock_user, follow_redirects=True)

        with patch('falken_drinks.routes.ControllerDrinkLogs.delete_drink_log_by_user', side_effect=Exception('boom')):
            response = self.client.delete('/api/delete_drink_log/1')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    import unittest
    unittest.main()
