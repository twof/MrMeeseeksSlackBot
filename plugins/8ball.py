from utils.constants import Plugin_Type
from Models.Message import Message
import random
from Plugin import Plugin


class Eight_Ball(Plugin):
    def __init__(self):
        super().__init__(Plugin_Type.starts_with, "/8")

    # message is of type message
    def callback(self, message):
        if message.content is self.query:
            return "Ask the magic 8ball a question! Usage: /8 <question>"

        messages = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it yes",
            "Most likely",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "God says no",
            "Very doubtful",
            "Outlook is terrible"
        ]

        return random.choice(messages)
