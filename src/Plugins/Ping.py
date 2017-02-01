from ..Models.Plugin import Plugin, Plugin_Type


class Ping(Plugin):
    def __init__(self):
        pattern = "p[io]ng"
        super().__init__(Plugin_Type.regex, pattern)

    def callback(self, message):
        if "ping" in message.content:
            return "pong"
        else:
            return "ping"

    def tests(self):
        cases = [("ping", "pong"),
                 ("pong", "ping"),
                 ("scrabble", "pong")]
        return cases
