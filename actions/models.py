import importlib
import json

from django.db import models

import mimesis.actions as actions
from mimesis.agent.agent import Agent

class Action(models.Model):
    name = models.CharField(max_length=256)
    identifier = models.CharField(max_length=256, default="Not set")
    description = models.CharField(max_length=512)
    prompt_instructions = models.CharField(max_length=512, null=True, blank=True)
    action_label = models.CharField(max_length=256, null=True, blank=True)
    follow_message = models.CharField(max_length=512, null=True, blank=True)
    previous_action = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey('agents.AgentDB', related_name='actions', on_delete=models.CASCADE, null=True, blank=True)
    mimesis_class = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_next_actions(self):
        return Action.objects.filter(previous_action=self)

    def call_agent(self, request):

        # Get submodule from mimesis_class
        module_name = self.mimesis_class.split(".")[0]
        mimesis_class_name = self.mimesis_class.split(".")[1]

        # Import the class of the action based on its name and submodule        
        submodule = importlib.import_module(f".{module_name}", actions.__name__)
        ActionClass = getattr(submodule, mimesis_class_name)
        action = ActionClass()

        # Load Agent from caché
        agent = Agent(**json.loads(request.session['agent']))
        agent.do(action)