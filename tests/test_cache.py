# by Richi Rod AKA @richionline / falken20

import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

from falken_drinks import cache


class TestCache(unittest.TestCase):

    @patch('falken_drinks.cache.Log.info')
    def test_cache(self, info_mock):
        cache.previous_cache = datetime.now()
        cache.check_cache()

        logged_messages = [call.args[0] for call in info_mock.call_args_list if call.args]
        self.assertTrue(any("Cache span" in message for message in logged_messages))

    @patch('falken_drinks.cache.Log.info')
    def test_cache_clean(self, info_mock):
        # Force cache age to exceed threshold without sleeping.
        cache.previous_cache = datetime.now() - timedelta(seconds=2)
        cache.check_cache(1)

        logged_messages = [call.args[0] for call in info_mock.call_args_list if call.args]
        self.assertTrue(any("Cleaning cache by expiration" in message for message in logged_messages))
