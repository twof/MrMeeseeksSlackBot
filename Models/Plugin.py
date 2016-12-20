# All plugins must implement this class
# Represents everything a plugin must have
#
# match_type: How the query can match messages.
#   represted in constants.Plugin_Type
# query: The string to match in accordance with match_type
# callback: function that will run on query match
from Utils.constants import Plugin_Type


# Plugin singleton
class Plugin(object):
    class _Plugin:
        def __init__(self, match_type=Plugin_Type.everything, query=None):
            self.match_type = match_type
            self.query = query

    instance = None

    def __init__(self, match_type=Plugin_Type.everything, query=None):
        if not Plugin.instance:
            Plugin.instance = Plugin._Plugin(match_type, query)
        else:
            Plugin.instance.match_type = match_type
            Plugin.instance.query = query
        self.match_type = match_type
        self.query = query

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def callback(reply, message):
        raise NotImplementedError("Subclass must implement abstract method")
