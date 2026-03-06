# by Richi Rod AKA @richionline / falken20

from datetime import date, datetime, timedelta

from .basetest import BaseTestCase
from falken_drinks.models import db, User, Drink, DrinkLog
from falken_drinks.controllers import ControllerUser, ControllerDrinks, ControllerDrinkLogs


class TestControllerUser(BaseTestCase):

    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(user.user_id)
        self.assertEqual(user.email, self.mock_user['email'])
        self.assertEqual(user.name, self.mock_user['name'])
        self.assertTrue(user.password)
        self.assertTrue(user.date_created)

    def test_delete_user(self):
        user = self.create_user()
        self.assertTrue(user.user_id)
        ControllerUser.delete_user(user.user_id)
        self.assertFalse(User.query.filter_by(user_id=user.user_id).first())

    def test_get_user(self):
        user = self.create_user()
        user_get = ControllerUser.get_user(user.user_id)
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


class TestControllerDrinks(BaseTestCase):

    def test_get_drink(self):
        """Test getting a drink by ID"""
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_get = ControllerDrinks.get_drink(drink.drink_id)
        self.assertEqual(drink_get.drink_name, 'Test Water')

    def test_get_drink_name(self):
        """Test getting a drink by name"""
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_get = ControllerDrinks.get_drink_name('Test Water')
        self.assertEqual(drink_get.drink_name, 'Test Water')

    def test_add_drink(self):
        """Test adding a new drink"""
        drink_data = {
            'drink_name': 'Test Beer',
            'drink_water_percentage': 95,
            'drink_alcohol_percentage': 5
        }
        drink = ControllerDrinks.add_drink(drink_data)
        
        self.assertIsNotNone(drink)
        self.assertEqual(drink.drink_name, 'Test Beer')
        self.assertEqual(drink.drink_water_percentage, 95)

    def test_get_or_create_drink_existing(self):
        """Test get_or_create with existing drink"""
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        result = ControllerDrinks.get_or_create_drink('Test Water', 0, 250)
        self.assertEqual(result.drink_id, drink.drink_id)

    def test_get_or_create_drink_new(self):
        """Test get_or_create with new drink"""
        result = ControllerDrinks.get_or_create_drink('New Drink', 5, 250)
        self.assertIsNotNone(result)
        self.assertEqual(result.drink_name, 'New Drink')

    def test_delete_drink(self):
        """Test deleting a drink"""
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        drink_id = drink.drink_id
        ControllerDrinks.delete_drink(drink_id)
        self.assertFalse(Drink.query.filter_by(drink_id=drink_id).first())

    def test_get_drink_not_found(self):
        """Test getting non-existent drink"""
        drink = ControllerDrinks.get_drink(999)
        self.assertIsNone(drink)

    def test_get_drinks(self):
        """Test getting all drinks"""
        drink1 = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        drink2 = Drink(drink_name='Beer', drink_water_percentage=95, drink_alcohol_percentage=5)
        db.session.add_all([drink1, drink2])
        db.session.commit()
        
        drinks = ControllerDrinks.get_drinks()
        self.assertGreaterEqual(len(drinks), 2)


class TestControllerDrinkLogs(BaseTestCase):

    def test_add_drink_log(self):
        """Test adding a drink log"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        log_data = {
            'drink_id': drink.drink_id,
            'user_id': user.user_id,
            'drink_total_quantity': 250,
            'drink_water_quantity': 250,
            'drink_alcohol_quantity': 0
        }
        
        log = ControllerDrinkLogs.add_drink_log(log_data)
        self.assertIsNotNone(log)
        self.assertEqual(log.drink_total_quantity, 250)

    def test_get_drink_logs_by_user(self):
        """Test getting drink logs for a user"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                      drink_total_quantity=250, drink_water_quantity=250,
                      drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()
        
        consumption = ControllerDrinkLogs.get_daily_consumption(user.user_id, date.today())
        self.assertIsNotNone(consumption)
        self.assertIn('total_liquid', consumption)

    def test_get_daily_summary(self):
        """Test getting daily summary"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0, counts_as_water=True)
        db.session.add(drink)
        db.session.commit()
        
        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                      drink_total_quantity=250, drink_water_quantity=250,
                      drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()
        
        summary = ControllerDrinkLogs.get_daily_summary(user.user_id, date.today())
        self.assertIsNotNone(summary)
        self.assertIn('total_logs', summary)
        self.assertGreater(summary['total_logs'], 0)

    def test_delete_drink_log_by_user(self):
        """Test deleting a drink log by user"""
        user = self.create_user()
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                      drink_total_quantity=250, drink_water_quantity=250,
                      drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()
        
        log_id = log.log_id
        result = ControllerDrinkLogs.delete_drink_log_by_user(log_id, user.user_id)
        self.assertTrue(result)
        self.assertFalse(DrinkLog.query.filter_by(log_id=log_id).first())

    def test_delete_drink_log_unauthorized(self):
        """Test deleting drink log with wrong user"""
        user1 = self.create_user()
        user2_data = {'email': 'user2@mail.com', 'name': 'user2', 'password': 'password'}
        user2 = self.create_user(user2_data)
        
        drink = Drink(drink_name='Test Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()
        
        log = DrinkLog(drink_id=drink.drink_id, user_id=user1.user_id,
                      drink_total_quantity=250, drink_water_quantity=250,
                      drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()
        
        # Try to delete with wrong user
        result = ControllerDrinkLogs.delete_drink_log_by_user(log.log_id, user2.user_id)
        self.assertFalse(result)

    def test_get_daily_consumption_with_multiple_drinks(self):
        """Test daily consumption calculation with multiple drinks"""
        user = self.create_user()
        
        # Create different drink types
        water = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0, counts_as_water=True)
        coffee = Drink(drink_name='Coffee', drink_water_percentage=98, drink_alcohol_percentage=0, counts_as_water=True)
        beer = Drink(drink_name='Beer', drink_water_percentage=95, drink_alcohol_percentage=5, counts_as_water=False)
        
        db.session.add_all([water, coffee, beer])
        db.session.commit()
        
        # Add logs for each drink
        log1 = DrinkLog(drink_id=water.drink_id, user_id=user.user_id,
                       drink_total_quantity=500, drink_water_quantity=500, drink_alcohol_quantity=0)
        log2 = DrinkLog(drink_id=coffee.drink_id, user_id=user.user_id,
                       drink_total_quantity=250, drink_water_quantity=245, drink_alcohol_quantity=0)
        log3 = DrinkLog(drink_id=beer.drink_id, user_id=user.user_id,
                       drink_total_quantity=330, drink_water_quantity=313, drink_alcohol_quantity=17)
        
        db.session.add_all([log1, log2, log3])
        db.session.commit()
        
        consumption = ControllerDrinkLogs.get_daily_consumption(user.user_id, date.today())
        
        self.assertIsNotNone(consumption)
        self.assertEqual(consumption['total_liquid'], 1080)
        self.assertGreater(consumption['total_water_for_progress'], 0)


class TestControllerDrinkLogsExtra(BaseTestCase):
    """Additional tests for controller methods not yet covered"""

    def test_get_drink_log_by_id(self):
        """Test getting a single drink log by ID"""
        user = self.create_user()
        drink = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                       drink_total_quantity=300, drink_water_quantity=300,
                       drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()

        result = ControllerDrinkLogs.get_drink_log(log.log_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.drink_total_quantity, 300)

    def test_get_drink_log_not_found(self):
        """Test getting a drink log that does not exist returns None"""
        result = ControllerDrinkLogs.get_drink_log(99999)
        self.assertIsNone(result)

    def test_get_all_drink_logs(self):
        """Test getting all drink logs returns a list"""
        user = self.create_user()
        drink = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()

        for qty in [100, 200, 300]:
            log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                           drink_total_quantity=qty, drink_water_quantity=qty,
                           drink_alcohol_quantity=0)
            db.session.add(log)
        db.session.commit()

        logs = ControllerDrinkLogs.get_drink_logs()
        self.assertGreaterEqual(len(logs), 3)

    def test_get_daily_consumption_empty(self):
        """Test daily consumption with no logs returns zeroed totals"""
        user = self.create_user()

        consumption = ControllerDrinkLogs.get_daily_consumption(user.user_id, date.today())
        self.assertIsNotNone(consumption)
        self.assertEqual(consumption['total_liquid'], 0)

    def test_delete_drink_log_direct(self):
        """Test the direct delete_drink_log method (not user-scoped)"""
        user = self.create_user()
        drink = Drink(drink_name='Water', drink_water_percentage=100, drink_alcohol_percentage=0)
        db.session.add(drink)
        db.session.commit()

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                       drink_total_quantity=250, drink_water_quantity=250,
                       drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()

        log_id = log.log_id
        ControllerDrinkLogs.delete_drink_log(log_id)
        self.assertIsNone(DrinkLog.query.filter_by(log_id=log_id).first())


class TestControllerDrinksExtra(BaseTestCase):
    """Additional tests for ControllerDrinks not yet covered"""

    def test_add_drink_with_counts_as_water_false(self):
        """Test adding a drink with counts_as_water=False"""
        drink_data = {
            'drink_name': 'Wine',
            'drink_water_percentage': 87,
            'drink_alcohol_percentage': 13,
            'counts_as_water': False
        }
        drink = ControllerDrinks.add_drink(drink_data)

        self.assertIsNotNone(drink)
        self.assertEqual(drink.drink_name, 'Wine')
        self.assertFalse(drink.counts_as_water)

    def test_add_drink_with_counts_as_water_true(self):
        """Test adding a drink with counts_as_water=True"""
        drink_data = {
            'drink_name': 'Herbal Tea',
            'drink_water_percentage': 99,
            'drink_alcohol_percentage': 0,
            'counts_as_water': True
        }
        drink = ControllerDrinks.add_drink(drink_data)

        self.assertIsNotNone(drink)
        self.assertTrue(drink.counts_as_water)

    def test_get_or_create_drink_calculates_water_percentage(self):
        """Test that get_or_create correctly calculates water percentage from alcohol"""
        result = ControllerDrinks.get_or_create_drink('Whisky', 40, 50)
        self.assertIsNotNone(result)
        self.assertEqual(result.drink_alcohol_percentage, 40)
        self.assertEqual(result.drink_water_percentage, 60)

    def test_get_drink_name_not_found(self):
        """Test get_drink_name returns None when drink doesn't exist"""
        result = ControllerDrinks.get_drink_name('NonExistentDrink')
        self.assertIsNone(result)


class TestGetFilteredAnalytics(BaseTestCase):
    """Tests for ControllerDrinkLogs.get_filtered_analytics()"""

    def _create_drink_and_log(self, user, drink_name='Water', water_pct=100, alcohol_pct=0,
                               total_qty=250, date_created=None):
        """Helper to create a drink and a log entry."""
        drink = Drink.query.filter_by(drink_name=drink_name).first()
        if not drink:
            drink = Drink(drink_name=drink_name, drink_water_percentage=water_pct,
                          drink_alcohol_percentage=alcohol_pct)
            db.session.add(drink)
            db.session.commit()

        water_qty = int(total_qty * water_pct / 100)
        alcohol_qty = int(total_qty * alcohol_pct / 100)
        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                       drink_total_quantity=total_qty, drink_water_quantity=water_qty,
                       drink_alcohol_quantity=alcohol_qty)
        db.session.add(log)
        db.session.flush()

        if date_created:
            log.date_created = date_created
        db.session.commit()
        return log

    # --- basic return structure ---

    def test_returns_expected_keys(self):
        """Result dict must have all required top-level keys."""
        user = self.create_user()
        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)
        for key in ('start_date', 'end_date', 'group_by', 'grouped_data',
                     'all_logs', 'total_logs', 'summary'):
            self.assertIn(key, result)

    def test_summary_keys(self):
        """Summary must contain the expected aggregation keys."""
        user = self.create_user()
        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)
        for key in ('total_liquid', 'total_water', 'total_alcohol',
                     'avg_daily_liquid', 'avg_daily_water'):
            self.assertIn(key, result['summary'])

    # --- empty data ---

    def test_no_logs_returns_zeros(self):
        """With no logs, totals and lists should be zero/empty."""
        user = self.create_user()
        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        self.assertEqual(result['total_logs'], 0)
        self.assertEqual(len(result['grouped_data']), 0)
        self.assertEqual(result['summary']['total_liquid'], 0)
        self.assertEqual(result['summary']['total_water'], 0)
        self.assertEqual(result['summary']['total_alcohol'], 0)

    # --- default date range ---

    def test_default_date_range_is_last_30_days(self):
        """Without explicit dates, range should be today minus 30 days."""
        user = self.create_user()
        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        self.assertEqual(result['end_date'], date.today())
        self.assertEqual(result['start_date'], date.today() - timedelta(days=30))

    # --- single log aggregation ---

    def test_single_water_log_aggregation(self):
        """A single water log should be correctly reflected in totals."""
        user = self.create_user()
        self._create_drink_and_log(user, 'Water', water_pct=100, alcohol_pct=0, total_qty=500)

        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        self.assertEqual(result['total_logs'], 1)
        self.assertEqual(result['summary']['total_liquid'], 500)
        self.assertEqual(result['summary']['total_water'], 500)
        self.assertEqual(result['summary']['total_alcohol'], 0)

    def test_single_alcohol_log_aggregation(self):
        """A single beer log should split water and alcohol correctly."""
        user = self.create_user()
        self._create_drink_and_log(user, 'Beer', water_pct=95, alcohol_pct=5, total_qty=330)

        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        self.assertEqual(result['summary']['total_liquid'], 330)
        self.assertEqual(result['summary']['total_water'], int(330 * 95 / 100))
        self.assertEqual(result['summary']['total_alcohol'], int(330 * 5 / 100))

    # --- multiple logs aggregation ---

    def test_multiple_logs_sum_correctly(self):
        """Multiple logs on the same day must be summed, not double-counted."""
        user = self.create_user()
        now = datetime.now()
        self._create_drink_and_log(user, 'Water', total_qty=250, date_created=now)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=now)

        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        self.assertEqual(result['summary']['total_liquid'], 550)
        self.assertEqual(result['total_logs'], 2)
        # Same day → one group
        self.assertEqual(len(result['grouped_data']), 1)
        self.assertEqual(result['grouped_data'][0]['log_count'], 2)

    # --- group_by day ---

    def test_group_by_day_creates_separate_groups(self):
        """Logs on different days should produce separate groups."""
        user = self.create_user()
        day1 = datetime(2025, 6, 1, 10, 0, 0)
        day2 = datetime(2025, 6, 2, 10, 0, 0)
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=day1)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=day2)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 2), group_by='day')

        self.assertEqual(len(result['grouped_data']), 2)
        self.assertEqual(result['total_logs'], 2)

    # --- group_by week ---

    def test_group_by_week_merges_same_week(self):
        """Two logs in the same ISO week should be in one group."""
        user = self.create_user()
        # Monday and Wednesday of the same week
        mon = datetime(2025, 6, 2, 10, 0, 0)  # Monday
        wed = datetime(2025, 6, 4, 10, 0, 0)  # Wednesday
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=mon)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=wed)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 7), group_by='week')

        self.assertEqual(len(result['grouped_data']), 1)
        self.assertEqual(result['grouped_data'][0]['total_liquid'], 500)
        self.assertEqual(result['grouped_data'][0]['log_count'], 2)

    def test_group_by_week_different_weeks(self):
        """Logs in different weeks should produce separate groups."""
        user = self.create_user()
        week1 = datetime(2025, 6, 2, 10, 0, 0)   # Week of Jun 2
        week2 = datetime(2025, 6, 10, 10, 0, 0)   # Week of Jun 9
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=week1)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=week2)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 15), group_by='week')

        self.assertEqual(len(result['grouped_data']), 2)

    # --- group_by month ---

    def test_group_by_month_merges_same_month(self):
        """Multiple logs in the same month should be in one group."""
        user = self.create_user()
        d1 = datetime(2025, 3, 5, 10, 0, 0)
        d2 = datetime(2025, 3, 20, 10, 0, 0)
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=d1)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=d2)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 3, 1), end_date=date(2025, 3, 31), group_by='month')

        self.assertEqual(len(result['grouped_data']), 1)
        self.assertEqual(result['grouped_data'][0]['total_liquid'], 500)

    # --- group_by year ---

    def test_group_by_year(self):
        """Logs in different years should produce separate groups."""
        user = self.create_user()
        d1 = datetime(2024, 6, 15, 10, 0, 0)
        d2 = datetime(2025, 6, 15, 10, 0, 0)
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=d1)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=d2)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2024, 1, 1), end_date=date(2025, 12, 31), group_by='year')

        self.assertEqual(len(result['grouped_data']), 2)
        self.assertEqual(result['total_logs'], 2)

    # --- sorting order ---

    def test_grouped_data_sorted_descending(self):
        """Grouped data should be sorted most recent first."""
        user = self.create_user()
        d1 = datetime(2025, 6, 1, 10, 0, 0)
        d2 = datetime(2025, 6, 3, 10, 0, 0)
        d3 = datetime(2025, 6, 2, 10, 0, 0)
        self._create_drink_and_log(user, 'Water', total_qty=100, date_created=d1)
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=d2)
        self._create_drink_and_log(user, 'Water', total_qty=150, date_created=d3)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 3), group_by='day')

        keys = [g['key'] for g in result['grouped_data']]
        self.assertEqual(keys, sorted(keys, reverse=True))

    # --- average daily calculation ---

    def test_avg_daily_liquid_calculation(self):
        """Average daily liquid = total_liquid / number_of_days_in_range."""
        user = self.create_user()
        start = date(2025, 6, 1)
        end = date(2025, 6, 3)  # 3 days
        self._create_drink_and_log(user, 'Water', total_qty=300,
                                    date_created=datetime(2025, 6, 1, 12, 0, 0))

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=start, end_date=end, group_by='day')

        days = (end - start).days + 1  # 3
        self.assertAlmostEqual(result['summary']['avg_daily_liquid'], 300 / days)

    # --- date range filtering ---

    def test_logs_outside_range_excluded(self):
        """Logs outside the specified date range should be excluded."""
        user = self.create_user()
        inside = datetime(2025, 6, 15, 10, 0, 0)
        outside = datetime(2025, 5, 1, 10, 0, 0)
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=inside)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=outside)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 30), group_by='day')

        self.assertEqual(result['total_logs'], 1)
        self.assertEqual(result['summary']['total_liquid'], 200)

    # --- user isolation ---

    def test_only_own_user_logs_returned(self):
        """Analytics should only include logs for the specified user."""
        user1 = self.create_user()
        user2_data = {'email': 'other@mail.com', 'name': 'other', 'password': 'password'}
        user2 = self.create_user(user2_data)

        self._create_drink_and_log(user1, 'Water', total_qty=500)
        self._create_drink_and_log(user2, 'Water', total_qty=300)

        result = ControllerDrinkLogs.get_filtered_analytics(user1.user_id)

        self.assertEqual(result['total_logs'], 1)
        self.assertEqual(result['summary']['total_liquid'], 500)

    # --- mixed drink types ---

    def test_mixed_drink_types_aggregation(self):
        """Water, beer and wine logs should aggregate correctly without double-counting."""
        user = self.create_user()
        now = datetime.now()
        self._create_drink_and_log(user, 'Water', water_pct=100, alcohol_pct=0,
                                    total_qty=500, date_created=now)
        self._create_drink_and_log(user, 'Beer', water_pct=95, alcohol_pct=5,
                                    total_qty=330, date_created=now)
        self._create_drink_and_log(user, 'Wine', water_pct=87, alcohol_pct=13,
                                    total_qty=150, date_created=now)

        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        self.assertEqual(result['summary']['total_liquid'], 500 + 330 + 150)
        expected_water = 500 + int(330 * 95 / 100) + int(150 * 87 / 100)
        expected_alcohol = 0 + int(330 * 5 / 100) + int(150 * 13 / 100)
        self.assertEqual(result['summary']['total_water'], expected_water)
        self.assertEqual(result['summary']['total_alcohol'], expected_alcohol)

    # --- log detail structure ---

    def test_log_detail_has_expected_keys(self):
        """Each log in grouped_data should have the expected detail keys."""
        user = self.create_user()
        self._create_drink_and_log(user, 'Water', total_qty=250)

        result = ControllerDrinkLogs.get_filtered_analytics(user.user_id)

        log_detail = result['grouped_data'][0]['logs'][0]
        for key in ('log_id', 'drink_name', 'total_quantity', 'water_quantity',
                     'alcohol_quantity', 'date_created', 'drink_image'):
            self.assertIn(key, log_detail)

    # --- invalid group_by defaults to day ---

    def test_invalid_group_by_defaults_to_day(self):
        """An unknown group_by value should fall back to day grouping."""
        user = self.create_user()
        d1 = datetime(2025, 6, 1, 10, 0, 0)
        d2 = datetime(2025, 6, 2, 10, 0, 0)
        self._create_drink_and_log(user, 'Water', total_qty=200, date_created=d1)
        self._create_drink_and_log(user, 'Water', total_qty=300, date_created=d2)

        result = ControllerDrinkLogs.get_filtered_analytics(
            user.user_id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 2),
            group_by='invalid_value')

        # Should still produce 2 groups (one per day), like 'day'
        self.assertEqual(len(result['grouped_data']), 2)


if __name__ == '__main__':
    import unittest
    unittest.main()
