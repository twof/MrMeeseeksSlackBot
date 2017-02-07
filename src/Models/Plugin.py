#!python
# -*- coding: utf-8 -*-
from ..Utils.constants import Plugin_Type
from ..Models.Singleton import Singleton
import importlib
import os
import re
from inspect import isclass, getmembers


class Plugin(Singleton):
    """
    All plugins must implement this class.

    match_type: How the query can match messages.
    Represted in constants.Plugin_Type

    query: The string to match in accordance with match_type

    callback: function that will run on query match
    """

    def __init__(self, match_type, query, followups_folder=None):
        self.match_type = match_type
        self.query = query
        self.followups = {}
        self.listeners = {}

        if followups_folder is not None:
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, '../Plugins/' + followups_folder)
            fls = os.listdir(filename)
            plug_files = [re.sub(r"\.pyc?", "", fl) for fl in fls
                          if fl.find(".py") != -1
                          and re.search(r"__init__|\.pyc", fl) is None]

            for plugin in plug_files:
                mod = "src.Plugins." + plugin
                new_mod = importlib.import_module(mod)

                plugin_classes = [plug[1]
                                  for plug in getmembers(new_mod, isclass)
                                  if issubclass(plug[1], Plugin)
                                  and plug[1] is not Plugin]

                if len(plugin_classes) == 0:
                    print(mod)
                    raise Exception("Plugin subclass not found")

                plugin_instance = plugin_classes[0]()
                c_name = plugin_instance.__class__.__name__

                self.followups[c_name] = plugin_instance

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

    def new_listener(self, user_name, context_arr, followup):
        self.listeners[user_name] = (context_arr, followup)

    def callback(self, message):
        raise NotImplementedError("Plugins must implement callback method")

    def tests(self):
        raise NotImplementedError("Plugins must implement tests method")

    def usage(self):
        raise NotImplementedError("Plugins must implement usage method")
