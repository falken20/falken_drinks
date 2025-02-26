# by Richi Rod AKA @richionline / falken20

from datetime import date
from io import StringIO
from unittest.mock import patch

from .basetest import BaseTestCase
from falken_plants.models import init_db, db, Plant, Calendar, User


class TestModelUser(BaseTestCase):
    def test_repr(self):
        self.assertIn('<User', str(User()))


class TestModelPlant(BaseTestCase):
    def test_repr(self):
        self.assertIn('<Plant', str(Plant(name='test', user_id=1)))

    def test_serialize(self):
        plant = Plant(name='test', user_id=1)
        self.assertEqual(plant.serialize(), {
            'id': None,
            'name': 'test',
            'name_tech': None,
            'comment': None,
            'watering_summer': 1,
            'watering_winter': 2,
            'spray': True,
            'direct_sun': 2,
            'image': None,
            'date_created': date.today(),
            'date_updated': date.today(),
            'user_id': 1
        })


class TestModelCalendar(BaseTestCase):
    #### Calendar model tests ####
    def test_repr(self):
        self.assertIn('<Calendar', str(Calendar()))


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
