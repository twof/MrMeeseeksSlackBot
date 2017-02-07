from src.Models.Plugin import Plugin, Plugin_Type


class Followup(Plugin):
    def __init__(self, plugin_type, pattern, followups_folder=None):
        super().__init__(Plugin_Type.regex, "^[0-9]+$", followups_folder)

    def callback(self, message, context_arr):
        raise NotImplementedError("Plugins must implement callback method")

    def tests(self):
        raise NotImplementedError("Plugins must implement tests method")

    def usage(self):
        raise NotImplementedError("Plugins must implement usage method")
