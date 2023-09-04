from django.db import models

from agents.models import AgentDB

class Chat(models.Model):
    """A chat is a conversation with an Agent.

    Attributes:
        name (str): The name of the chat.
        description (str): The description of the chat.
    """

    name = models.CharField(max_length=256)
    agent = models.ForeignKey(AgentDB, on_delete=models.CASCADE)

    def __str__(self):
        return self.name