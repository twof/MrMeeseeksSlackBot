import Plugins
import importlib
import inspect
from Utils.constants import Plugin_Type

plugin_arr = []


def setup():
    for plugin in Plugins.__all__:
        mod = "Plugins." + plugin
        new_mod = importlib.import_module(mod)
        plugin_class = inspect.getmembers(new_mod)[0]
        plugin_arr.append(plugin_class[1])


# plugin is a class which makes things a bit wonky
def handle(message):
    for plugin in plugin_arr:
        return{
            Plugin_Type.everything: _everything(message, plugin()),
            Plugin_Type.equals: _equals(message, plugin()),
            Plugin_Type.starts_with: _starts_with(message, plugin()),
            Plugin_Type.contains: _contains(message, plugin()),
        }.get(plugin().match_type, None)


def _everything(message, plugin):
    return plugin.callback(message)


def _equals(message, plugin):
    if message.content is plugin.query:
        return plugin.callback(message)


def _starts_with(message, plugin):
    if message.content.startswith(plugin.query):
        return plugin.callback(message)


def _contains(message, plugin):
    if plugin.query in message.content:
        return plugin.callback(message)
