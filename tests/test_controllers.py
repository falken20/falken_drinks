# by Richi Rod AKA @richionline / falken20
from datetime import date

from .basetest import BaseTestCase
from falken_plants.models import db, User, Plant, Calendar
from falken_plants.controllers import ControllerPlant, ControllerCalendar, ControllerUser


class TestControllerUser(BaseTestCase):
    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(user.id)
        self.assertEqual(user.email, self.mock_user['email'])
        self.assertEqual(user.name, self.mock_user['name'])
        self.assertTrue(user.password)
        self.assertTrue(user.date_created)

    def test_delete_user(self):
        user = self.create_user()
        self.assertTrue(user.id)
        ControllerUser.delete_user(user.id)
        self.assertFalse(User.query.filter_by(id=user.id).first())

    def test_get_user(self):
        user = self.create_user()
        user_get = ControllerUser.get_user(user.id)
        self.assertEqual(user_get.email, user.email)

    def test_get_user_email(self):
        user = self.create_user()
        user_get = ControllerUser.get_user_email(user.email)
        self.assertEqual(user_get.email, user.email)

    def test_get_user_name(self):
        user = self.create_user()
        user_get = ControllerUser.get_user_name(user.name)
        self.assertEqual(user_get.name, user.name)

    def test_get_user_no_user(self):
        user = ControllerUser.get_user(1)
        self.assertFalse(user)


class TestControllerPlant(BaseTestCase):

    MOCK_PLANT = {'id': 100, 'name': 'test_plant_mock', 'name_tech': 'test_plant_mock', 'comment': 'test_plant_mock',
                'watering_summer': 2, 'watering_winter': 2, 'spray': True, 'direct_sun': 2, 'image': ''}

    def test_create_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        self.assertTrue(plant.id)
        self.assertEqual(plant.name, self.MOCK_PLANT['name'])
        self.assertEqual(plant.name_tech, self.MOCK_PLANT['name_tech'])
        self.assertEqual(plant.comment, self.MOCK_PLANT['comment'])
        self.assertEqual(plant.watering_summer, self.MOCK_PLANT['watering_summer'])
        self.assertEqual(plant.watering_winter, self.MOCK_PLANT['watering_winter'])
        self.assertTrue(plant.spray)
        self.assertEqual(plant.direct_sun, self.MOCK_PLANT['direct_sun'])
        self.assertTrue(plant.date_created)
        self.assertEqual(plant.user_id, user.id)

    def test_get_plants(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        plants = ControllerPlant.list_all_plants(user.id)
        self.assertEqual(len(plants), 1)
        self.assertEqual(plants[0].name, plant.name)

    def test_get_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        plant_get = ControllerPlant.get_plant(plant.id)
        self.assertEqual(plant_get.name, plant.name)

    def test_get_plant_name(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        plant_get = ControllerPlant.get_plant_name(plant.name)
        self.assertEqual(plant_get.name, plant.name)

    def test_update_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        plant.name = 'test_plant_update'
        plant.name_tech = 'test_plant_update'
        plant.comment = 'test_plant_update'
        plant.watering_summer = 2
        plant.watering_winter = 2
        plant.spray = False
        plant.direct_sun = 2

        plant_update = ControllerPlant.update_plant(plant.__dict__, user.id)
        
        self.assertEqual(plant_update.name, 'test_plant_update')
        self.assertEqual(plant_update.name_tech, 'test_plant_update')
        self.assertEqual(plant_update.comment, 'test_plant_update')
        self.assertEqual(plant_update.watering_summer, 2)
        self.assertEqual(plant_update.watering_winter, 2)
        self.assertFalse(plant_update.spray)
        self.assertEqual(plant_update.direct_sun, 2)

    def test_update_plant_no_user(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        ControllerUser.delete_user(user.id)        
        self.assertRaises(ValueError, ControllerPlant.update_plant, plant.serialize(), user.id)

    def test_delete_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)
        ControllerPlant.delete_plant(plant.id)
        self.assertFalse(Plant.query.filter_by(id=plant.id).first())

    def test_create_plant_no_name(self):
        user = self.create_user()
        # Copy with copy() to avoid changing the original dict
        mock_plant = self.MOCK_PLANT.copy()
        mock_plant['name'] = ''
        print(f"================================= MOCK_PLANT: {mock_plant}")
        self.assertRaises(ValueError, ControllerPlant.create_plant, mock_plant, current_user=user.id)

    def test_create_plant_no_user(self):
        mock_plant = self.MOCK_PLANT
        self.assertRaises(ValueError, ControllerPlant.create_plant, mock_plant, current_user=None)
        self.assertRaises(ValueError, ControllerPlant.create_plant, mock_plant, current_user=5)

    def test_get_plants_no_user(self):
        user = self.create_user()
        plants = ControllerPlant.list_all_plants(user_id=user.id)
        self.assertEqual(len(plants), 0)

    def test_get_plants_no_plants(self):
        user = self.create_user()
        plants = ControllerPlant.list_all_plants(user.id)
        self.assertFalse(plants)

    def test_get_plant_no_plant(self):
        plant = ControllerPlant.get_plant(1)
        self.assertFalse(plant)

    def test_get_plant_name_no_plant(self):
        plant = ControllerPlant.get_plant_name('test_plant')
        self.assertFalse(plant)

    def test_update_plant_no_plant(self):
        user = self.create_user()
        plant_update = ControllerPlant.update_plant(self.MOCK_PLANT, user.id)
        self.assertFalse(plant_update)

    def test_delete_plant_no_plant(self):
        plant_delete = ControllerPlant.delete_plant(10)
        self.assertFalse(plant_delete)


class TestControllerCalendar(BaseTestCase):

    MOCK_PLANT = {'id': 100, 'name': 'test_plant_mock', 'name_tech': 'test_plant_mock', 'comment': 'test_plant_mock',
                'watering_summer': 2, 'watering_winter': 2, 'spray': True, 'direct_sun': 2, 'image': ''}

    def test_create_calendar(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)
        calendar = ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        self.assertTrue(calendar)
        self.assertEqual(calendar.plant_id, plant.id)
        self.assertEqual(calendar.date_calendar, date.today())

    def test_get_calendar(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        calendar_get = ControllerCalendar.get_calendar(plant_id=plant.id)
        self.assertIsInstance(calendar_get, list)
        self.assertEqual(calendar_get[0].plant_id, plant.id)

    def test_get_calendar_date(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        calendar_get = ControllerCalendar.get_calendar_date(
            plant_id=plant.id, date_calendar=date.today())
        self.assertIsInstance(calendar_get, Calendar)
        self.assertEqual(calendar_get.plant_id, plant.id)
        self.assertEqual(calendar_get.date_calendar, date.today())

    def test_delete_calendar_date(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        ControllerCalendar.delete_calendar_date(
            plant_id=plant.id, date_calendar=date.today())
        calendar_get = ControllerCalendar.get_calendar_date(
            date_calendar=date.today(), plant_id=plant.id)
        self.assertFalse(calendar_get)
        # Test delete calendar None
        calendar_delete = ControllerCalendar.delete_calendar_date(
            plant_id=plant.id, date_calendar=date.today())
        self.assertFalse(calendar_delete)

    def test_delete_calendar_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        ControllerCalendar.delete_calendar_plant(plant_id=plant.id)
        calendar_get = ControllerCalendar.get_calendar(plant_id=plant.id)
        self.assertFalse(calendar_get)
        # Test delete calendar plant None
        calendar_delete = ControllerCalendar.delete_calendar_plant(
            plant_id=plant.id)
        self.assertFalse(calendar_delete)
