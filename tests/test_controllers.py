# by Richi Rod AKA @richionline / falken20# by Richi Rod AKA @richionline / falken20

from datetime import datefrom datetime import date



from .basetest import BaseTestCasefrom .basetest import BaseTestCase

from falken_drinks.models import db, User, Drink, DrinkLogfrom falken_drinks.models import db, User, Drink, DrinkLog

from falken_drinks.controllers import ControllerUser, ControllerDrinks, ControllerDrinkLogsfrom falken_drinks.controllers import ControllerUser, ControllerDrinks, ControllerDrinkLogs





class TestControllerUser(BaseTestCase):class TestControllerUser(BaseTestCase):

    def test_get_user(self):    def test_create_user(self):

        user = self.create_user()        user = self.create_user()

        user_get = ControllerUser.get_user(user.user_id)        self.assertTrue(user.id)

        self.assertEqual(user_get.email, user.email)        self.assertEqual(user.email, self.mock_user['email'])

        self.assertEqual(user.name, self.mock_user['name'])

    def test_get_user_email(self):        self.assertTrue(user.password)

        user = self.create_user()        self.assertTrue(user.date_created)

        user_get = ControllerUser.get_user_email(user.email)

        self.assertEqual(user_get.email, user.email)    def test_delete_user(self):

        user = self.create_user()

    def test_get_user_name(self):        self.assertTrue(user.id)

        user = self.create_user()        ControllerUser.delete_user(user.id)

        user_get = ControllerUser.get_user_name(user.name)        self.assertFalse(User.query.filter_by(id=user.id).first())

        self.assertEqual(user_get.name, user.name)

    def test_get_user(self):

    def test_get_user_no_user(self):        user = self.create_user()

        user = ControllerUser.get_user(999)        user_get = ControllerUser.get_user(user.id)

        self.assertFalse(user)        self.assertEqual(user_get.email, user.email)



    def test_delete_user(self):    def test_get_user_email(self):

        user = self.create_user()        user = self.create_user()

        self.assertTrue(user.user_id)        user_get = ControllerUser.get_user_email(user.email)

        ControllerUser.delete_user(user.user_id)        self.assertEqual(user_get.email, user.email)

        self.assertFalse(User.query.filter_by(user_id=user.user_id).first())

    def test_get_user_name(self):

        user = self.create_user()

class TestControllerDrinks(BaseTestCase):        user_get = ControllerUser.get_user_name(user.name)

        self.assertEqual(user_get.name, user.name)

    def test_get_drink(self):

        """Test getting a drink by ID"""    def test_get_user_no_user(self):

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)        user = ControllerUser.get_user(1)

        db.session.add(drink)        self.assertFalse(user)

        db.session.commit()

        

        drink_get = ControllerDrinks.get_drink(drink.drink_id)class TestControllerPlant(BaseTestCase):

        self.assertEqual(drink_get.drink_name, 'Test Water')

    MOCK_PLANT = {'id': 100, 'name': 'test_plant_mock', 'name_tech': 'test_plant_mock', 'comment': 'test_plant_mock',

    def test_get_drink_name(self):                'watering_summer': 2, 'watering_winter': 2, 'spray': True, 'direct_sun': 2, 'image': ''}

        """Test getting a drink by name"""

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)    def test_create_plant(self):

        db.session.add(drink)        user = self.create_user()

        db.session.commit()        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

                self.assertTrue(plant.id)

        drink_get = ControllerDrinks.get_drink_name('Test Water')        self.assertEqual(plant.name, self.MOCK_PLANT['name'])

        self.assertEqual(drink_get.drink_name, 'Test Water')        self.assertEqual(plant.name_tech, self.MOCK_PLANT['name_tech'])

        self.assertEqual(plant.comment, self.MOCK_PLANT['comment'])

    def test_get_drinks(self):        self.assertEqual(plant.watering_summer, self.MOCK_PLANT['watering_summer'])

        """Test getting all drinks"""        self.assertEqual(plant.watering_winter, self.MOCK_PLANT['watering_winter'])

        drink1 = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)        self.assertTrue(plant.spray)

        drink2 = Drink(drink_name='Coffee', drink_water_percentage=90, drink_alcohol_percentage=0)        self.assertEqual(plant.direct_sun, self.MOCK_PLANT['direct_sun'])

        db.session.add(drink1)        self.assertTrue(plant.date_created)

        db.session.add(drink2)        self.assertEqual(plant.user_id, user.id)

        db.session.commit()

            def test_get_plants(self):

        drinks = ControllerDrinks.get_drinks()        user = self.create_user()

        self.assertEqual(len(drinks), 2)        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

        plants = ControllerPlant.list_all_plants(user.id)

    def test_add_drink(self):        self.assertEqual(len(plants), 1)

        """Test adding a new drink"""        self.assertEqual(plants[0].name, plant.name)

        drink_data = {

            'drink_name': 'Test Beer',    def test_get_plant(self):

            'drink_water_percentage': 95,        user = self.create_user()

            'drink_alcohol_percentage': 5        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

        }        plant_get = ControllerPlant.get_plant(plant.id)

        drink = ControllerDrinks.add_drink(drink_data)        self.assertEqual(plant_get.name, plant.name)

        self.assertIsNotNone(drink)

        self.assertEqual(drink.drink_name, 'Test Beer')    def test_get_plant_name(self):

        self.assertEqual(drink.drink_water_percentage, 95)        user = self.create_user()

        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

    def test_get_or_create_drink_existing(self):        plant_get = ControllerPlant.get_plant_name(plant.name)

        """Test get_or_create with existing drink"""        self.assertEqual(plant_get.name, plant.name)

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)

        db.session.add(drink)    def test_update_plant(self):

        db.session.commit()        user = self.create_user()

                plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

        result = ControllerDrinks.get_or_create_drink('Test Water', 0, 250)        plant.name = 'test_plant_update'

        self.assertEqual(result.drink_id, drink.drink_id)        plant.name_tech = 'test_plant_update'

        plant.comment = 'test_plant_update'

    def test_get_or_create_drink_new(self):        plant.watering_summer = 2

        """Test get_or_create with new drink"""        plant.watering_winter = 2

        result = ControllerDrinks.get_or_create_drink('New Drink', 5, 250)        plant.spray = False

        self.assertIsNotNone(result)        plant.direct_sun = 2

        self.assertEqual(result.drink_name, 'New Drink')

        plant_update = ControllerPlant.update_plant(plant.__dict__, user.id)

    def test_delete_drink(self):        

        """Test deleting a drink"""        self.assertEqual(plant_update.name, 'test_plant_update')

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)        self.assertEqual(plant_update.name_tech, 'test_plant_update')

        db.session.add(drink)        self.assertEqual(plant_update.comment, 'test_plant_update')

        db.session.commit()        self.assertEqual(plant_update.watering_summer, 2)

                self.assertEqual(plant_update.watering_winter, 2)

        drink_id = drink.drink_id        self.assertFalse(plant_update.spray)

        ControllerDrinks.delete_drink(drink_id)        self.assertEqual(plant_update.direct_sun, 2)

        self.assertFalse(Drink.query.filter_by(drink_id=drink_id).first())

    def test_update_plant_no_user(self):

    def test_get_drink_not_found(self):        user = self.create_user()

        """Test getting non-existent drink"""        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

        drink = ControllerDrinks.get_drink(999)        ControllerUser.delete_user(user.id)        

        self.assertIsNone(drink)        self.assertRaises(ValueError, ControllerPlant.update_plant, plant.serialize(), user.id)



    def test_delete_plant(self):

class TestControllerDrinkLogs(BaseTestCase):        user = self.create_user()

        plant = ControllerPlant.create_plant(self.MOCK_PLANT, user.id)

    def test_add_drink_log(self):        ControllerPlant.delete_plant(plant.id)

        """Test adding a drink log"""        self.assertFalse(Plant.query.filter_by(id=plant.id).first())

        user = self.create_user()

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)    def test_create_plant_no_name(self):

        db.session.add(drink)        user = self.create_user()

        db.session.commit()        # Copy with copy() to avoid changing the original dict

                mock_plant = self.MOCK_PLANT.copy()

        log_data = {        mock_plant['name'] = ''

            'drink_id': drink.drink_id,        print(f"================================= MOCK_PLANT: {mock_plant}")

            'user_id': user.user_id,        self.assertRaises(ValueError, ControllerPlant.create_plant, mock_plant, current_user=user.id)

            'drink_total_quantity': 250,

            'drink_water_quantity': 250,    def test_create_plant_no_user(self):

            'drink_alcohol_quantity': 0        mock_plant = self.MOCK_PLANT

        }        self.assertRaises(ValueError, ControllerPlant.create_plant, mock_plant, current_user=None)

                self.assertRaises(ValueError, ControllerPlant.create_plant, mock_plant, current_user=5)

        log = ControllerDrinkLogs.add_drink_log(log_data)

        self.assertIsNotNone(log)    def test_get_plants_no_user(self):

        self.assertEqual(log.drink_total_quantity, 250)        user = self.create_user()

        plants = ControllerPlant.list_all_plants(user_id=user.id)

    def test_get_drink_logs_by_user(self):        self.assertEqual(len(plants), 0)

        """Test getting drink logs for a user"""

        user = self.create_user()    def test_get_plants_no_plants(self):

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)        user = self.create_user()

        db.session.add(drink)        plants = ControllerPlant.list_all_plants(user.id)

        db.session.commit()        self.assertFalse(plants)

        

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,    def test_get_plant_no_plant(self):

                      drink_total_quantity=250, drink_water_quantity=250,        plant = ControllerPlant.get_plant(1)

                      drink_alcohol_quantity=0)        self.assertFalse(plant)

        db.session.add(log)

        db.session.commit()    def test_get_plant_name_no_plant(self):

                plant = ControllerPlant.get_plant_name('test_plant')

        logs = ControllerDrinkLogs.get_drink_logs_by_user(user.user_id, date.today())        self.assertFalse(plant)

        self.assertGreater(len(logs), 0)

    def test_update_plant_no_plant(self):

    def test_get_daily_summary(self):        user = self.create_user()

        """Test getting daily summary"""        plant_update = ControllerPlant.update_plant(self.MOCK_PLANT, user.id)

        user = self.create_user()        self.assertFalse(plant_update)

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)

        db.session.add(drink)    def test_delete_plant_no_plant(self):

        db.session.commit()        plant_delete = ControllerPlant.delete_plant(10)

                self.assertFalse(plant_delete)

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,

                      drink_total_quantity=250, drink_water_quantity=250,

                      drink_alcohol_quantity=0)class TestControllerCalendar(BaseTestCase):

        db.session.add(log)

        db.session.commit()    MOCK_PLANT = {'id': 100, 'name': 'test_plant_mock', 'name_tech': 'test_plant_mock', 'comment': 'test_plant_mock',

                        'watering_summer': 2, 'watering_winter': 2, 'spray': True, 'direct_sun': 2, 'image': ''}

        summary = ControllerDrinkLogs.get_daily_summary(user.user_id, date.today())

        self.assertIsNotNone(summary)    def test_create_calendar(self):

        self.assertIn('total_logs', summary)        user = self.create_user()

        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)

    def test_delete_drink_log_by_user(self):        calendar = ControllerCalendar.create_calendar(

        """Test deleting a drink log by user"""            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)

        user = self.create_user()        self.assertTrue(calendar)

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)        self.assertEqual(calendar.plant_id, plant.id)

        db.session.add(drink)        self.assertEqual(calendar.date_calendar, date.today())

        db.session.commit()

            def test_get_calendar(self):

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,        user = self.create_user()

                      drink_total_quantity=250, drink_water_quantity=250,        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)

                      drink_alcohol_quantity=0)        ControllerCalendar.create_calendar(

        db.session.add(log)            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)

        db.session.commit()        calendar_get = ControllerCalendar.get_calendar(plant_id=plant.id)

                self.assertIsInstance(calendar_get, list)

        log_id = log.log_id        self.assertEqual(calendar_get[0].plant_id, plant.id)

        result = ControllerDrinkLogs.delete_drink_log_by_user(log_id, user.user_id)

        self.assertTrue(result)    def test_get_calendar_date(self):

        self.assertFalse(DrinkLog.query.filter_by(log_id=log_id).first())        user = self.create_user()

        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)

    def test_delete_drink_log_unauthorized(self):        ControllerCalendar.create_calendar(

        """Test deleting drink log with wrong user"""            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)

        user1 = self.create_user()        calendar_get = ControllerCalendar.get_calendar_date(

        user2_data = {'email': 'user2@mail.com', 'name': 'user2', 'password': 'password'}            plant_id=plant.id, date_calendar=date.today())

        user2 = self.create_user(user2_data)        self.assertIsInstance(calendar_get, Calendar)

                self.assertEqual(calendar_get.plant_id, plant.id)

        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)        self.assertEqual(calendar_get.date_calendar, date.today())

        db.session.add(drink)

        db.session.commit()    def test_delete_calendar_date(self):

                user = self.create_user()

        log = DrinkLog(drink_id=drink.drink_id, user_id=user1.user_id,        plant = ControllerPlant.create_plant(self.MOCK_PLANT, current_user=user.id)

                      drink_total_quantity=250, drink_water_quantity=250,        ControllerCalendar.create_calendar(

                      drink_alcohol_quantity=0)            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)

        db.session.add(log)        ControllerCalendar.delete_calendar_date(

        db.session.commit()            plant_id=plant.id, date_calendar=date.today())

                calendar_get = ControllerCalendar.get_calendar_date(

        # Try to delete with wrong user            date_calendar=date.today(), plant_id=plant.id)

        result = ControllerDrinkLogs.delete_drink_log_by_user(log.log_id, user2.user_id)        self.assertFalse(calendar_get)

        self.assertFalse(result)        # Test delete calendar None

        calendar_delete = ControllerCalendar.delete_calendar_date(

            plant_id=plant.id, date_calendar=date.today())

if __name__ == '__main__':        self.assertFalse(calendar_delete)

    import unittest

    unittest.main()    def test_delete_calendar_plant(self):

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
