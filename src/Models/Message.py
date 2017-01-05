class Message:
    def __init__(self, content=None, sender_id=None, channel=None):
        self.content = content
        self.sender_id = sender_id
        self.channel = channel
