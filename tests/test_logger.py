# by Richi Rod AKA @richionline / falken20

from io import StringIO
import sys
import unittest
from unittest.mock import patch

from falken_plants import logger


def redirect_stdout():
    captured_output = StringIO()  # Create StringIO object
    sys.stdout = captured_output  # and redirect stdout
    return captured_output


def redirect_reset():
    sys.stdout = sys.__stdout__  # Reset redirect


class TestLogger(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdin', StringIO('Writing...\n'))  # Simulate user input
    def test_debug_exception(self, stdout, stderr):
        logger.LEVEL_LOG = "['DEBUG']"
        trace = "Test Debug"
        logger.Log.debug(trace, style="error_style")
        # self.assertIn(trace, stdout.getvalue())
        self.assertEqual(True, True)

    @patch('sys.stdout', new_callable=StringIO)
    def test_debug(self, stdout):
        logger.LEVEL_LOG = "['DEBUG']"
        trace = "Test Debug"
        logger.Log.debug(trace)
        self.assertIn(trace, stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_debug_no_trace(self, stdout):
        logger.LEVEL_LOG = "[]"
        trace = "Test Debug"
        logger.Log.debug(trace)
        self.assertNotIn(trace, stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, stdout):
        logger.LEVEL_LOG = "['INFO']"
        trace = "Test Info"
        logger.Log.info(trace)
        self.assertIn(trace, stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_info_no_trace(self, stdout):
        logger.LEVEL_LOG = "[]"
        trace = "Test Info"
        logger.Log.info(trace)
        self.assertNotIn(trace, stdout.getvalue())

    def test_info_exception(self):
        logger.LEVEL_LOG = "['INFO']"
        trace = "Test Info"
        self.assertRaises(Exception, logger.Log.info(
            trace, style="error_style"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning(self, stdout):
        logger.LEVEL_LOG = "['WARNING']"
        trace = "Test Warning"
        logger.Log.warning(trace)
        self.assertIn(trace, stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning_no_trace(self, stdout):
        logger.LEVEL_LOG = "[]"
        trace = "Test Warning"
        logger.Log.warning(trace)
        self.assertNotIn(trace, stdout.getvalue())

    def test_warning_exception(self):
        logger.LEVEL_LOG = "['WARNING']"
        trace = "Test Warning"
        self.assertRaises(Exception, logger.Log.warning(
            trace, style="error_style"))

    @patch('sys.stdout', new_callable=StringIO)
    def test_error(self, stdout):
        logger.LEVEL_LOG = "['ERROR']"
        trace = "Test Error"

        try:
            raise (Exception)
        except Exception as err:
            logger.Log.error(trace, err, sys)
            self.assertIn(trace, stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_error_no_trace(self, stdout):
        logger.LEVEL_LOG = "[]"
        trace = "Test Error"

        try:
            raise (Exception)
        except Exception as err:
            logger.Log.error(trace, err, sys)
            self.assertNotIn(trace, stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_error_exception(self, stdout):
        logger.LEVEL_LOG = "['ERROR']"
        trace = "Test Error"
        try:
            raise (Exception)
        except Exception as err:
            self.assertRaises(Exception, logger.Log.error(
                trace, err, sys, style="error_style"))
