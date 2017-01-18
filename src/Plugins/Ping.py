from ..Utils.constants import Plugin_Type
from ..Models.Plugin import Plugin
from ..Models.Singleton import Singleton


class Ping(Plugin, Singleton):
    def __init__(self):
        pattern = "p[io]ng"
        super().__init__(Plugin_Type.regex, pattern)

    def callback(self, message):
        if "ping" in message.content:
            return "pong"
        else:
            return "ping"
