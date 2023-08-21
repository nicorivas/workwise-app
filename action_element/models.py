import importlib
import json
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from actions.models import Action
from instruction.models import Instruction

from mimesis.agent.agent import Agent
import mimesis.actions as actions

class ActionElementType(models.Model):

    class ActionElementTypes(models.TextChoices):
        MESSAGE = "MSG", _("Message")
        TEXT_INPUT = "TXT", _("Text Input")
        AGENT_CALL = "ACA", _("Agent Call")

    name = models.CharField(max_length=3, choices=ActionElementTypes.choices, default=ActionElementTypes.MESSAGE)
    description = models.TextField()

    def __str__(self):
        return self.name

    def template(self):
        if self.name == self.ActionElementTypes.MESSAGE:
            return "action_element/instruction/message.html"
        elif self.name == self.ActionElementTypes.TEXT_INPUT:
            return "action_element/instruction/text_input.html"
        elif self.name == self.ActionElementTypes.AGENT_CALL:
            return "action_element/instruction/agent_call.html"

class ActionElement(models.Model):
    """An action element is an element of an action, part of an instruction.
    """

    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    type = models.ForeignKey(ActionElementType, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    guide = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def template(self):
        return self.type.template()
    
class ActionElementTextInput(ActionElement):

    message = models.TextField(null=True, blank=True)
    audio = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ActionElementType.objects.get(name=ActionElementType.ActionElementTypes.TEXT_INPUT)

    def __str__(self):
        return self.name
    
    def template(self):
        return self.type.template()

class ActionElementMessage(ActionElement):

    message = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ActionElementType.objects.get(name=ActionElementType.ActionElementTypes.MESSAGE)

    def __str__(self):
        return self.name
    
    def template(self):
        return self.type.template()

class ActionElementAgentCall(ActionElement):

    button_label = models.CharField(max_length=256, default="Submit")
    mimesis_action = models.CharField(max_length=256, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ActionElementType.objects.get(name=ActionElementType.ActionElementTypes.AGENT_CALL)

    def __str__(self):
        return self.name
    
    def call_agent(self, request):
        print(f"ActionElementAgentCall.call_agent() called: {request.POST}")

        # Get all inputs from action
        # For now we only have text inputs
        text_inputs = ActionElementTextInput.objects.filter(action=self.action)
        action_parameters = {}
        for text_input in text_inputs:
            # Update the action element with information from the request, that comes from the form.
            # The name of the text_input is always the name of the element in the form
            text_input.message = request.POST[text_input.name]
            text_input.save()
            action_parameters[text_input.name] = request.POST[text_input.name]

        # Get submodule of action or chain from mimesis_class, that is, the name of the class (with module name).
        module_name = self.mimesis_action.split(".")[0]
        mimesis_class_name = self.mimesis_action.split(".")[1]

        # Import the class of the action based on its name and submodule 
        submodule = importlib.import_module(f".{module_name}", actions.__name__)
        ActionClass = getattr(submodule, mimesis_class_name)
        # Here is where we initialize the action with the parameters from the form
        actionClass = ActionClass(**action_parameters)

        # Load Agent from caché
        agent = Agent(**json.loads(request.session['agent']))

        # Execute action in mimesis
        logging.info(f"Calling Mimesis action {actionClass}")
        reply = agent.do(actionClass)

        return reply