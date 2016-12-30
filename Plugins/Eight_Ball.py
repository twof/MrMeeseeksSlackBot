from Utils.constants import Plugin_Type
import random
from Models.Plugin import Plugin
from Models.Singleton import Singleton


# All plugins must implement Plugin and Singleton
class Eight_Ball(Plugin, Singleton):
    def __init__(self):
        super(Eight_Ball, self).__init__(Plugin_Type.starts_with, "/8")

    # message is of type Message
    def callback(self, message):
        print(message.content)
        if message.content == self.query:
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
