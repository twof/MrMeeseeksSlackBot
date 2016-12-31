from Utils.constants import Plugin_Type
from Models.Plugin import Plugin
from Models.Singleton import Singleton


class Ping(Plugin, Singleton):
    def __init__(self):
        super(Ping, self).__init__(Plugin_Type.regex, "p[io]ng")

    def callback(self, message):
        if "ping" in message.content:
            return "pong"
        else:
            return "ping"
