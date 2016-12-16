# All plugins must implement this class
class Plugin:
    def __init__(self, match_type, query):
        self.match_type = match_type
        self.query = query

    def callback(self, reply, message):
        raise NotImplementedError("Subclass must implement abstract method")
