import unittest
import pytest

from . import basetest
from falken_drinks.models import db, Drink, DrinkLog


class TestMain(basetest.BaseTestCase):

    def test_index(self):
        """Test GET / renders home page"""
        self.create_user()
        self.login_http(self)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_home_alias(self):
        """Test GET /home also renders home page"""
        self.create_user()
        self.login_http(self)

        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_index_unauthorized(self):
        """Test GET / redirects to login when not authenticated"""
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    @pytest.mark.skip(reason="show_grouped route has been removed/deprecated")
    def test_show_grouped(self):
        self.create_user()
        self.login_http(self)

        response = self.client.get('/show_grouped/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        """Test GET /profile renders profile page"""
        self.create_user()
        self.login_http(self)

        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)

    def test_profile_unauthorized(self):
        """Test GET /profile redirects to login when not authenticated"""
        response = self.client.get('/profile', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_daily_summary(self):
        """Test GET /daily_summary renders daily summary page"""
        self.create_user()
        self.login_http(self)

        response = self.client.get('/daily_summary')
        self.assertEqual(response.status_code, 200)

    def test_daily_summary_with_logs(self):
        """Test GET /daily_summary with existing drink logs"""
        user = self.create_user()
        self.login_http(self)

        drink = Drink(drink_name='Water', drink_water_percentage=100,
                      drink_alcohol_percentage=0, counts_as_water=True)
        db.session.add(drink)
        db.session.commit()

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                       drink_total_quantity=500, drink_water_quantity=500,
                       drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()

        response = self.client.get('/daily_summary')
        self.assertEqual(response.status_code, 200)

    def test_daily_summary_unauthorized(self):
        """Test GET /daily_summary redirects to login when not authenticated"""
        response = self.client.get('/daily_summary', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_analytics_get(self):
        """Test GET /analytics renders analytics page with default date range"""
        self.create_user()
        self.login_http(self)

        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)

    def test_analytics_get_with_data(self):
        """Test GET /analytics renders correctly with drink logs data"""
        user = self.create_user()
        self.login_http(self)

        drink = Drink(drink_name='Water', drink_water_percentage=100,
                      drink_alcohol_percentage=0, counts_as_water=True)
        db.session.add(drink)
        db.session.commit()

        log = DrinkLog(drink_id=drink.drink_id, user_id=user.user_id,
                       drink_total_quantity=500, drink_water_quantity=500,
                       drink_alcohol_quantity=0)
        db.session.add(log)
        db.session.commit()

        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)

    def test_analytics_post_with_filters(self):
        """Test POST /analytics with date range and group_by filters"""
        self.create_user()
        self.login_http(self)

        form_data = {
            'start_date': '2026-01-01',
            'end_date': '2026-02-28',
            'group_by': 'week'
        }
        response = self.client.post('/analytics', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_analytics_post_group_by_month(self):
        """Test POST /analytics grouped by month"""
        self.create_user()
        self.login_http(self)

        form_data = {
            'start_date': '2026-01-01',
            'end_date': '2026-03-01',
            'group_by': 'month'
        }
        response = self.client.post('/analytics', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_analytics_post_invalid_dates(self):
        """Test POST /analytics with invalid date strings falls back gracefully"""
        self.create_user()
        self.login_http(self)

        form_data = {
            'start_date': 'not-a-date',
            'end_date': 'also-not-a-date',
            'group_by': 'day'
        }
        response = self.client.post('/analytics', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_analytics_unauthorized(self):
        """Test GET /analytics redirects to login when not authenticated"""
        response = self.client.get('/analytics', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_drinks_management(self):
        """Test GET /drinks_management renders drinks management page"""
        self.create_user()
        self.login_http(self)

        response = self.client.get('/drinks_management')
        self.assertEqual(response.status_code, 200)

    def test_drinks_management_with_drinks(self):
        """Test GET /drinks_management renders correctly when drinks exist"""
        self.create_user()
        self.login_http(self)

        drink = Drink(drink_name='Water', drink_water_percentage=100,
                      drink_alcohol_percentage=0, counts_as_water=True)
        db.session.add(drink)
        db.session.commit()

        response = self.client.get('/drinks_management')
        self.assertEqual(response.status_code, 200)

    def test_drinks_management_unauthorized(self):
        """Test GET /drinks_management redirects to login when not authenticated"""
        response = self.client.get('/drinks_management', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])
