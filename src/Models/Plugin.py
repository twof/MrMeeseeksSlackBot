#!python
# -*- coding: utf-8 -*-
from ..Utils.constants import Plugin_Type
from ..Models.Singleton import Singleton
import re


class Plugin(Singleton):
    """
    All plugins must implement this class.

    match_type: How the query can match messages.
    Represted in constants.Plugin_Type

    query: The string to match in accordance with match_type

    callback: function that will run on query match
    """

    def __init__(self, match_type, query):
        self.match_type = match_type
        self.query = query

    def _everything(self, message):
        return self.callback(message)

    def _equals(self, message):
        if message.content is self.query:
            return self.callback(message)

    def _starts_with(self, message):
        if message.content.startswith(self.query):
            return self.callback(message)

    def _contains(self, message):
        if self.query in message.content:
            return self.callback(message)

    def _regex(self, message):
        if re.search(self.query, message.content) is not None:
            return self.callback(message)

    def callback(reply, message):
        raise NotImplementedError("Plugins must implement callback method")

    def tests(self):
        raise NotImplementedError("Plugins must implement tests method")

    def handle(self, message):
        match = self.match_type

        if match is Plugin_Type.equals:
            response = self._equals(message)
        elif match is Plugin_Type.contains:
            response = self._contains(message)
        elif match is Plugin_Type.starts_with:
            response = self._starts_with(message)
        elif match is Plugin_Type.everything:
            response = self._everything(message)
        elif match is Plugin_Type.regex:
            response = self._regex(message)
        else:
            return None

        return response if response else None
