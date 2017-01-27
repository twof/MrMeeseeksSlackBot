from ..Models.Plugin import Plugin, Plugin_Type
import random


# All plugins must implement Plugin and Singleton
class Eight_Ball(Plugin):
    '''
    Will only trigger on messages that start with ".8"
    This is indicated by the Plugin_Type being starts_with and the query being
    .8.
    Examples:
    Will match:
    ".8 Are you sentient?"
    ".8"
    Will not match:
    "Are you sentient?"
    "\8 Are you sentient?"
    "fasdfs.8 Are you sentient?"
    '''
    def __init__(self):
        prefix = ".8"
        super().__init__(Plugin_Type.starts_with, prefix)

    '''
    Triggered when the query is matched by a message. Tha message is wrapped as
    an object and passed in the callback as a parameter.
    '''
    def callback(self, message):
        '''
        Example of a helpful hint in the event of near correct usage
        Triggers when the message starts with the correct query but a question
        wasn't asked.
        Example:
        ".8"
        '''
        if message.content == self.query:
            return "Ask the magic 8ball a question! Usage: .8 <question>"

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

        '''Returns one of the above responses at random'''
        return random.choice(messages)
