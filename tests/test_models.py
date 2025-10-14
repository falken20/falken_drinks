# by Richi Rod AKA @richionline / falken20

from datetime import date
from io import StringIO
from unittest.mock import patch

from .basetest import BaseTestCase
from falken_drinks.models import init_db, db, User, Drink, DrinkLog


class TestModelUser(BaseTestCase):
    def test_repr(self):
        self.assertIn('<User', str(User()))

    def test_user_serialize(self):
        """Test User serialize method"""
        user = User(email='test@test.com', name='Test User', password='password123')
        serialized = user.serialize()
        self.assertIsInstance(serialized, dict)
        self.assertIn('email', serialized)
        self.assertIn('name', serialized)


class TestModelDrink(BaseTestCase):
    def test_repr(self):
        self.assertIn('<Drink', str(Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)))

    def test_serialize(self):
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        serialized = drink.serialize()
        self.assertEqual(serialized['drink_name'], 'Test Water')
        self.assertEqual(serialized['drink_water_percentage'], 100)
        self.assertEqual(serialized['drink_alcohol_percentage'], 0)

    def test_validate_name(self):
        """Test drink name validation"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name=None, drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()

    def test_validate_percentage(self):
        """Test drink percentage validation"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='Test', drink_water_percentage=150, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()


class TestModelDrinkLog(BaseTestCase):
    def test_repr(self):
        """Test DrinkLog repr method"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0)
        self.assertIn('<DrinkLog', str(drink_log))

    def test_serialize(self):
        """Test DrinkLog serialize method"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0)
        db.session.add(drink_log)
        db.session.commit()
        
        serialized = drink_log.serialize()
        self.assertIsInstance(serialized, dict)
        self.assertEqual(serialized['drink_total_quantity'], 250)
        self.assertEqual(serialized['drink_water_quantity'], 250)


class TestInitDB(BaseTestCase):
    #### init_db tests ####
    def test_init_db_vars(self):
        self.assertTrue(db)
        self.assertTrue(self.app)

    @patch('sys.stdin', StringIO('testing\nN\nN\n'))  # Simulate user input
    def test_init_db_with_answer_N(self):
        init_db(self.app)

    @patch('sys.stdin', StringIO('testing\nY\nY\n'))  # Simulate user input
    def test_init_db_with_drops(self):
        init_db(self.app)

    @patch('sys.stdin', StringIO('testing\nN\nY\n'))  # Simulate user input
    def test_init_db_with_create(self):
        init_db(self.app)

    @patch('sys.stdin', StringIO('XXXX\nY\nN\n'))  # Simulate user input
    def test_init_db_with_wrong_input(self):
        init_db(self.app)
        self.assertRaises(ValueError)
