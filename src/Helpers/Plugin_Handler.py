import importlib
import os
import re
from inspect import isclass, getmembers
from ..Models.Plugin import Plugin

plugin_arr = []


def setup():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../Plugins')
    fls = os.listdir(filename)
    plug_files = [re.sub(r"\.pyc?", "", fl) for fl in fls
                  if fl.find(".py") != -1
                  and re.search(r"__init__|\.pyc", fl) is None]

    for plugin in plug_files:
        mod = "src.Plugins." + plugin
        new_mod = importlib.import_module(mod)

        plugin_classes = [plug[1] for plug in getmembers(new_mod, isclass)
                          if issubclass(plug[1], Plugin)
                          and plug[1] is not Plugin]

        if len(plugin_classes) == 0:
            print(mod)
            raise Exception("Plugin subclass not found")

        plugin_instance = plugin_classes[0]()
        plugin_arr.append(plugin_instance)


def handle(message):
    responses = []

    for plugin in plugin_arr:
        if message.sender_id in plugin.listeners:
            response = plugin.listeners[message.sender_id][1].handle(message)
        else:
            response = plugin.handle(message)

        if response:
            responses.append(response)

    return responses if responses else None
