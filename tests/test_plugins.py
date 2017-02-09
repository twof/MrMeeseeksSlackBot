import unittest
from src.Helpers import Plugin_Handler
from src.Models.Message import Message
from dotenv import load_dotenv
import os


class PluginsTest(unittest.TestCase):
    def setUp(self):
        # Load environment variables
        load_dotenv(os.path.join('.', '.env'))

        self.handler = Plugin_Handler
        self.handler.setup()

    def test_run_plugin_test(self):
        for plugin in self.handler.plugin_arr:
            for case in plugin.tests():
                assert plugin.handle(Message(case[0])),\
                    "Test case " + str(case)\
                    + " does not conform to the query"\
                    + " for plugin " + type(plugin).__name__

                if len(case) < 2:
                    print("Test case " + str(case)
                          + " for plugin " + type(plugin).__name__
                          + " sent back:")
                    print(plugin.callback(Message(case[0])))
                elif type(case[1]) == bool:
                    assert bool(plugin.callback(Message(case[0]))) == case[1],\
                        "Failed on " + type(plugin).__name__\
                        + " on test case " + str(case)
                else:
                    assert plugin.callback(Message(case[0])) == case[1],\
                        "Failed on " + type(plugin).__name__\
                        + " on test case " + str(case)
