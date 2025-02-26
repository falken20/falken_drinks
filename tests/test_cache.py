# by Richi Rod AKA @richionline / falken20

import unittest
from io import StringIO
from unittest.mock import patch
import time

from falken_plants import cache

class TestCache(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_cache(self, stdout):
        cache.check_cache()
        self.assertIn("Cache span", stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_cache_clean(self, stdout):
        cache.check_cache()
        time.sleep(2)
        cache.check_cache(1)
        self.assertIn("Cleaning cache by expiration", stdout.getvalue())
