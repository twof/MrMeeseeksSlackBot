import importlib
from inspect import isclass
from .. import Plugins
from ..Models.Plugin import Plugin

plugin_arr = []


def setup():
    for plugin in Plugins.__all__:
        mod = "src.Plugins." + plugin
        new_mod = importlib.import_module(mod)

        classes = [getattr(new_mod, subclass) for subclass in dir(new_mod)
                   if isclass(getattr(new_mod, subclass))]
        plugin_classes = [subclass for subclass in classes
                          if issubclass(subclass, Plugin)
                          and subclass is not Plugin]
        if len(plugin_classes) == 0:
            raise Exception("Plugin subclass not found")

        plugin_instance = plugin_classes[0]()
        plugin_arr.append(plugin_instance)


def handle(message):
    responses = []

    for plugin in plugin_arr:
        response = plugin.handle(message)

        if response:
            responses.append(response)

    return responses if responses else None
