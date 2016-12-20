# All plugins must implement this class
# Represents everything a plugin must have
#
# match_type: How the query can match messages.
#   represted in constants.Plugin_Type
# query: The string to match in accordance with match_type
# callback: function that will run on query match
from Utils.constants import Plugin_Type


class Plugin(object):
    def __init__(self, match_type=Plugin_Type.everything, query=None):
        self.match_type = match_type
        self.query = query

    def callback(reply, message):
        raise NotImplementedError("Subclass must implement abstract method")
