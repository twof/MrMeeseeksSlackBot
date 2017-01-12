import unittest
from ..src.Helpers import Plugin_Handler


class FlaskServerTest(unittest.TestCase):
    def setUp(self):
        self.handler = Plugin_Handler

    def test_setup(self):
        self.handler.setup()
        print(self.handler.plugin_arr)
