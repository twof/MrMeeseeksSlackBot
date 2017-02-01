import unittest
from src.Helpers import Plugin_Handler
from src.Models.Message import Message


class PluginsTest(unittest.TestCase):
    def setUp(self):
        self.handler = Plugin_Handler
        self.handler.setup()

    def test_run_plugin_test(self):
        for plugin in self.handler.plugin_arr:
            for case in plugin.tests():
                assert plugin.handle(Message(case[0])),\
                    "Test case " + str(case)\
                    + " does not conform to the query"\
                    + " for plugin " + type(plugin).__name__

                if type(case[1]) == bool:
                    assert bool(plugin.callback(Message(case[0]))) == case[1],\
                        "Failed on " + type(plugin).__name__\
                        + " on test case " + str(case)
                else:
                    assert plugin.callback(Message(case[0])) == case[1],\
                        "Failed on " + type(plugin).__name__\
                        + " on test case " + str(case)
