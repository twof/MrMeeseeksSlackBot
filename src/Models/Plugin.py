#!python
# -*- coding: utf-8 -*-
from ..Utils.constants import Plugin_Type
from ..Models.Singleton import Singleton
from inspect import isclass, getmembers
import importlib
import os
import re


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
                mod = "src.Plugins." + followups_folder + "." + plugin
                new_mod = importlib.import_module(mod)

                plugin_classes = [plug[1]
                                  for plug in getmembers(new_mod, isclass)
                                  if issubclass(plug[1], Plugin)
                                  and plug[1] is not Plugin]

                if len(plugin_classes) == 0:
                    raise Exception("Plugin subclass not found")

                plugin_instance = plugin_classes[0]()
                c_name = plugin_instance.__class__.__name__

                self.followups[c_name] = plugin_instance

    def _everything(self, message, context_arr=[]):
        return self.callback(message, context_arr)\
            if context_arr else self.callback(message)

    def _equals(self, message, context_arr=[]):
        if message.content is self.query:
            return self.callback(message, context_arr)\
                if context_arr else self.callback(message)

    def _starts_with(self, message, context_arr=[]):
        if message.content.startswith(self.query):
            return self.callback(message, context_arr)\
                if context_arr else self.callback(message)

    def _contains(self, message, context_arr=[]):
        if self.query in message.content:
            return self.callback(message, context_arr)\
                if context_arr else self.callback(message)

    def _regex(self, message, context_arr=[]):
        if re.search(self.query, message.content) is not None:
            return self.callback(message, context_arr)\
                if context_arr else self.callback(message)

    def handle(self, message, context_arr=[]):
        match = self.match_type

        print(self.__class__.__name__)
        print(context_arr)

        if not context_arr:
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
        else:
            print(self.__class__.__name__)
            print(context_arr)
            if match is Plugin_Type.equals:
                response = self._equals(message, context_arr)
            elif match is Plugin_Type.contains:
                response = self._contains(message, context_arr)
            elif match is Plugin_Type.starts_with:
                response = self._starts_with(message, context_arr)
            elif match is Plugin_Type.everything:
                response = self._everything(message, context_arr)
            elif match is Plugin_Type.regex:
                response = self._regex(message, context_arr)
            else:
                return None

        return response if response else None

    def new_listener(self, user_name, context_arr, followup):
        self.listeners[user_name] = (context_arr, followup)

    def remove_listener(self, user_name):
        self.listeners.pop(user_name)

    def callback(self, message, context_arr=[]):
        raise NotImplementedError("Plugins must implement callback method")

    def tests(self):
        raise NotImplementedError("Plugins must implement tests method")

    def usage(self):
        raise NotImplementedError("Plugins must implement usage method")
