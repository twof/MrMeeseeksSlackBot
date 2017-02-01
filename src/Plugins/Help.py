from ..Models.Plugin import Plugin, Plugin_Type
from ..Helpers import Plugin_Handler


class Help(Plugin):
    def __init__(self):
        query = ".help"
        super().__init__(Plugin_Type.starts_with, query)

    def callback(self, message):
        usage = [(type(plugin).__name__ + ":\n\t" + plugin.usage())
                 for plugin in Plugin_Handler.plugin_arr]

        return "\n".join(usage)

    def tests(self):
        cases = [(".help", True),
                 (".help asfasdf", True)]
        return cases

    def usage(self):
        return "usage: .help -> sends usage for all plugins"
