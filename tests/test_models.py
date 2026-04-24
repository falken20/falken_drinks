# by Richi Rod AKA @richionline / falken20

from datetime import date
from io import StringIO
from unittest.mock import patch

from .basetest import BaseTestCase
from falken_drinks.models import init_db, db, User, Drink, DrinkLog


class TestModelUser(BaseTestCase):
    def test_repr(self):
        self.assertIn('<User', str(User()))

    def test_user_str(self):
        """Test User __str__ method"""
        user = User(email='test@test.com', name='TestUser', password='password123')
        db.session.add(user)
        db.session.commit()
        self.assertIn('<User', str(user))
        self.assertIn('TestUser', str(user))

    def test_user_serialize(self):
        """Test User serialize method excludes password field"""
        user = User(email='test@test.com', name='Test User', password='password123')
        db.session.add(user)
        db.session.commit()
        serialized = user.serialize()
        self.assertIsInstance(serialized, dict)
        self.assertIn('email', serialized)
        self.assertIn('name', serialized)
        self.assertNotIn('password', serialized)  # password must be excluded for security
        self.assertIn('user_id', serialized)
        self.assertEqual(serialized['email'], 'test@test.com')
        self.assertEqual(serialized['name'], 'Test User')

    def test_user_get_id(self):
        """Test User get_id method returns string user_id"""
        user = User(email='test@test.com', name='Test User', password='password123')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.get_id(), str(user.user_id))

    def test_user_password_hash_fits_model_limit(self):
        user = User(email='test@test.com', name='Test User', password='x' * 103)
        self.assertEqual(user.password, 'x' * 103)

    def test_user_password_max_length(self):
        """Test User password at max allowed length (255 chars)"""
        max_pass = 'x' * 255
        user = User(email='test@test.com', name='Test User', password=max_pass)
        self.assertEqual(user.password, max_pass)

    def test_user_password_too_long(self):
        """Test User password exceeds max length (256 chars)"""
        with self.assertRaises(ValueError):
            User(email='test@test.com', name='Test User', password='x' * 256)

    def test_user_email_too_long(self):
        with self.assertRaises(ValueError):
            User(email=('a' * 101) + '@mail.com', name='Test User', password='password123')

    def test_user_name_too_long(self):
        with self.assertRaises(ValueError):
            User(email='test@test.com', name='a' * 101, password='password123')

    def test_user_email_none_raises_error(self):
        """Test User email None raises ValueError"""
        with self.assertRaises(ValueError):
            User(email=None, name='Test User', password='password123')

    def test_user_email_blank_raises_error(self):
        """Test User email blank/whitespace raises ValueError"""
        with self.assertRaises(ValueError):
            User(email='   ', name='Test User', password='password123')

    def test_user_name_none_allowed(self):
        """Test User name can be None (optional field)"""
        user = User(email='test@test.com', name=None, password='password123')
        db.session.add(user)
        db.session.commit()
        self.assertIsNone(user.name)

    def test_user_name_blank_raises_error(self):
        """Test User name blank/whitespace raises ValueError"""
        with self.assertRaises(ValueError):
            User(email='test@test.com', name='   ', password='password123')

    def test_user_password_none_raises_error(self):
        """Test User password None raises ValueError"""
        with self.assertRaises(ValueError):
            User(email='test@test.com', name='Test User', password=None)

    def test_user_password_blank_raises_error(self):
        """Test User password blank/whitespace raises ValueError"""
        with self.assertRaises(ValueError):
            User(email='test@test.com', name='Test User', password='   ')

    def test_user_email_whitespace_stripped(self):
        """Test User email whitespace is stripped"""
        user = User(email='  test@test.com  ', name='Test User', password='password123')
        self.assertEqual(user.email, 'test@test.com')

    def test_user_name_whitespace_stripped(self):
        """Test User name whitespace is stripped"""
        user = User(email='test@test.com', name='  Test User  ', password='password123')
        self.assertEqual(user.name, 'Test User')


class TestModelDrink(BaseTestCase):
    def test_repr(self):
        self.assertIn('<Drink', str(Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)))

    def test_drink_str(self):
        """Test Drink __str__ method"""
        drink = Drink(drink_name='Beer', drink_water_percentage=95, drink_alcohol_percentage=5)
        self.assertIn('<Drink', str(drink))
        self.assertIn('Beer', str(drink))
        self.assertIn('95%', str(drink))
        self.assertIn('5%', str(drink))

    def test_serialize(self):
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        serialized = drink.serialize()
        self.assertEqual(serialized['drink_name'], 'Test Water')
        self.assertEqual(serialized['drink_water_percentage'], 100)
        self.assertEqual(serialized['drink_alcohol_percentage'], 0)
        self.assertIn('drink_id', serialized)
        self.assertIn('counts_as_water', serialized)

    def test_validate_name(self):
        """Test drink name validation"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name=None, drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()

    def test_validate_name_blank(self):
        """Test drink name blank raises error"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='   ', drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()

    def test_validate_percentage(self):
        """Test drink percentage validation"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='Test', drink_water_percentage=150, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()

    def test_validate_percentage_negative(self):
        """Test drink percentage cannot be negative"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='Test', drink_water_percentage=-10, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()

    def test_validate_percentage_alcohol_over_100(self):
        """Test alcohol percentage over 100 raises error"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='Test', drink_water_percentage=50, drink_alcohol_percentage=101)
            db.session.add(drink)
            db.session.commit()

    def test_validate_percentage_not_integer(self):
        """Test percentage must be integer"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='Test', drink_water_percentage=50.5, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()

    def test_counts_as_water_default_no_alcohol(self):
        """Test counts_as_water defaults to True when no alcohol"""
        drink = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        self.assertTrue(drink.counts_as_water)

    def test_counts_as_water_default_with_alcohol(self):
        """Test counts_as_water defaults to False when alcohol > 0"""
        drink = Drink(drink_name='Beer', drink_water_percentage=95, drink_alcohol_percentage=5)
        self.assertFalse(drink.counts_as_water)

    def test_counts_as_water_explicitly_true(self):
        """Test counts_as_water can be explicitly set to True"""
        drink = Drink(drink_name='Special', drink_water_percentage=95, 
                     drink_alcohol_percentage=5, counts_as_water=True)
        self.assertTrue(drink.counts_as_water)

    def test_counts_as_water_explicitly_false(self):
        """Test counts_as_water can be explicitly set to False"""
        drink = Drink(drink_name='Water', drink_water_percentage=100, 
                     drink_alcohol_percentage=0, counts_as_water=False)
        self.assertFalse(drink.counts_as_water)

    def test_drink_image_empty_string_becomes_none(self):
        """Test empty string for drink_image is converted to None"""
        drink = Drink(drink_name='Water', drink_water_percentage=100, 
                     drink_alcohol_percentage=0, drink_image='')
        self.assertIsNone(drink.drink_image)

    def test_drink_image_valid_string(self):
        """Test drink_image accepts valid string"""
        drink = Drink(drink_name='Water', drink_water_percentage=100, 
                     drink_alcohol_percentage=0, drink_image='water.png')
        self.assertEqual(drink.drink_image, 'water.png')

    def test_drink_image_none(self):
        """Test drink_image accepts None"""
        drink = Drink(drink_name='Water', drink_water_percentage=100, 
                     drink_alcohol_percentage=0, drink_image=None)
        self.assertIsNone(drink.drink_image)


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

    def test_drink_log_str(self):
        """Test DrinkLog __str__ method"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0)
        db.session.add(drink_log)
        db.session.commit()
        log_str = str(drink_log)
        self.assertIn('<DrinkLog', log_str)
        self.assertIn('250', log_str)

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
        self.assertIn('log_id', serialized)
        self.assertIn('drink_id', serialized)
        self.assertIn('user_id', serialized)
        self.assertIn('date_created', serialized)

    def test_drink_log_validate_drink_id_none(self):
        """Test DrinkLog drink_id None raises ValueError"""
        with self.assertRaises(ValueError):
            user = self.create_user()
            drink_log = DrinkLog(drink_id=None, user_id=user.user_id,
                                drink_total_quantity=250, drink_water_quantity=250,
                                drink_alcohol_quantity=0)
            db.session.add(drink_log)
            db.session.commit()

    def test_drink_log_validate_user_id_none(self):
        """Test DrinkLog user_id None raises ValueError"""
        with self.assertRaises(ValueError):
            drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()
            drink_log = DrinkLog(drink_id=drink.drink_id, user_id=None,
                                drink_total_quantity=250, drink_water_quantity=250,
                                drink_alcohol_quantity=0)
            db.session.add(drink_log)
            db.session.commit()

    def test_drink_log_validate_total_quantity_none(self):
        """Test DrinkLog total_quantity None raises ValueError"""
        with self.assertRaises(ValueError):
            user = self.create_user()
            drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()
            drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                                drink_total_quantity=None, drink_water_quantity=250,
                                drink_alcohol_quantity=0)
            db.session.add(drink_log)
            db.session.commit()

    def test_drink_log_validate_water_quantity_none(self):
        """Test DrinkLog water_quantity None raises ValueError"""
        with self.assertRaises(ValueError):
            user = self.create_user()
            drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()
            drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                                drink_total_quantity=250, drink_water_quantity=None,
                                drink_alcohol_quantity=0)
            db.session.add(drink_log)
            db.session.commit()

    def test_drink_log_validate_alcohol_quantity_none(self):
        """Test DrinkLog alcohol_quantity None raises ValueError"""
        with self.assertRaises(ValueError):
            user = self.create_user()
            drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
            db.session.add(drink)
            db.session.commit()
            drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                                drink_total_quantity=250, drink_water_quantity=250,
                                drink_alcohol_quantity=None)
            db.session.add(drink_log)
            db.session.commit()

    def test_drink_log_date_created_default(self):
        """Test DrinkLog date_created defaults to now_cet_naive"""
        user = self.create_user()
        drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0)
        db.session.add(drink_log)
        db.session.commit()
        
        # Check that date_created is set and is near now
        self.assertIsNotNone(drink_log.date_created)
        from datetime import datetime, timedelta
        now = datetime.now()
        diff = now - drink_log.date_created
        # Should be created within last minute
        self.assertLess(diff, timedelta(minutes=1))

    def test_drink_log_date_created_custom(self):
        """Test DrinkLog date_created can be set to a custom value"""
        user = self.create_user()
        drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        custom_date = date(2025, 1, 15)
        from datetime import datetime
        custom_datetime = datetime(2025, 1, 15, 12, 0, 0)
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=250, drink_water_quantity=250,
                            drink_alcohol_quantity=0, date_created=custom_datetime)
        db.session.add(drink_log)
        db.session.commit()
        
        self.assertEqual(drink_log.date_created, custom_datetime)

    def test_drink_log_quantities_zero(self):
        """Test DrinkLog accepts zero quantities"""
        user = self.create_user()
        drink = Drink(drink_name='Test', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                            drink_total_quantity=0, drink_water_quantity=0,
                            drink_alcohol_quantity=0)
        db.session.add(drink_log)
        db.session.commit()
        
        self.assertEqual(drink_log.drink_total_quantity, 0)
        self.assertEqual(drink_log.drink_water_quantity, 0)
        self.assertEqual(drink_log.drink_alcohol_quantity, 0)


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
