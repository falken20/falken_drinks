# by Richi Rod AKA @richionline / falken20

import unittest
from datetime import date
from unittest.mock import patch

from falken_drinks import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        config.get_settings.cache_clear()
        config.print_app_config.cache_clear()

    def test_get_settings(self):
        settings = config.get_settings()
        self.assertIsInstance(settings, config.Settings)

    def test_get_settings_is_cached(self):
        first = config.get_settings()
        second = config.get_settings()
        self.assertIs(first, second)

    def test_now_cet_has_timezone(self):
        current = config.now_cet()
        self.assertIsNotNone(current.tzinfo)

    def test_now_cet_naive_has_no_timezone(self):
        current = config.now_cet_naive()
        self.assertIsNone(current.tzinfo)

    def test_today_cet_returns_date(self):
        today = config.today_cet()
        self.assertIsInstance(today, date)

    def test_day_bounds_returns_start_and_end_of_day(self):
        from datetime import datetime
        target = date(2026, 4, 24)
        start, end = config.day_bounds(target)
        self.assertEqual(start, datetime(2026, 4, 24, 0, 0, 0))
        self.assertEqual(end.year, 2026)
        self.assertEqual(end.month, 4)
        self.assertEqual(end.day, 24)
        self.assertEqual(end.hour, 23)
        self.assertEqual(end.minute, 59)
        self.assertLess(start, end)

    def test_shorten_url_returns_same_url(self):
        url = 'https://example.com/some/path'
        self.assertEqual(config.shorten_url(url), url)

    def test_settings_app_data_populated(self):
        settings = config.Settings()
        self.assertIn('title', settings.APP_DATA)
        self.assertIn('version', settings.APP_DATA)
        self.assertIn('author', settings.APP_DATA)
        self.assertIn('description', settings.APP_DATA)

    def test_get_params_from_toml_contains_project(self):
        settings = config.Settings()
        data = settings.get_params_from_toml()
        self.assertIn('project', data)
        self.assertIn('version', data['project'])

    def test_development_config_database_uri(self):
        self.assertTrue(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'))

    def test_testing_config_database_uri_is_string(self):
        self.assertIsInstance(config.TestingConfig.SQLALCHEMY_DATABASE_URI, str)

    def test_production_config_database_uri_is_string(self):
        self.assertIsInstance(config.ProductionConfig.SQLALCHEMY_DATABASE_URI, str)

    def test_config_repr_and_str(self):
        cfg = config.TestingConfig()
        self.assertEqual(repr(cfg), 'Config()')
        self.assertIsInstance(str(cfg), str)

    def test_print_settings_environment_calls_log_info_dict(self):
        with patch('falken_drinks.config.Log.info_dict') as mock_info_dict:
            config.print_settings_environment(config.TestingConfig)
        mock_info_dict.assert_called_once()

    def test_print_app_config_logs_values(self):
        class FakeApp:
            config = {
                'SIMPLE': 'value',
                'NESTED': {
                    'testing': config.TestingConfig,
                    'plain': 123
                }
            }

        with patch('falken_drinks.config.Log.info') as mock_info:
            config.print_app_config(FakeApp())

        self.assertGreater(mock_info.call_count, 0)

    def test_print_app_config_is_cached(self):
        class FakeApp:
            config = {'A': 'B'}

        with patch('falken_drinks.config.Log.info') as mock_info:
            app = FakeApp()
            config.print_app_config(app)
            first_count = mock_info.call_count
            config.print_app_config(app)
            self.assertEqual(mock_info.call_count, first_count)
