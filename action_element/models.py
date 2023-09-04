import importlib
import json
import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from actions.models import Action
from instruction.models import InstructionType

from mimesis.agent.agent import Agent
import mimesis.actions.actions as actions

from django.templatetags.static import static


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
    """An action element is an element of an instruction, which constructs actions.

    It is an abstract element, think of it as a form element.

    Attributes:
        action (Action): The action that the element belongs to.
        instruction_type (InstructionType): The instruction type that the element belongs to.
        index (int): The index of the element in the instruction type.
        type (ActionElementType): The type of the element.
        name (str): The name of the element.
        guide (str): The guide of the element.
    """

    instruction_type = models.ForeignKey(InstructionType, on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    type = models.ForeignKey(ActionElementType, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    guide = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.instruction_type.name} - {self.type} - {self.name}"
    
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
    document_input = models.CharField(max_length=256, null=True, blank=True)
    working_message = models.CharField(max_length=256, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = ActionElementType.objects.get(name=ActionElementType.ActionElementTypes.AGENT_CALL)

    def __str__(self):
        return self.name
    
    def call_agent(self, request, instruction):
        print(f"ActionElementAgentCall.call_agent() called: {request.POST}")

        # Update instruction data based on POST, that is, the form values
        instruction.update(request.POST)

        # The parameters to give to the agent action are held in the instruction data, that is, the values of the form.
        action_parameters = instruction.data

        # Get submodule of action or chain from mimesis_class, that is, the name of the class (with module name).
        #module_name = self.mimesis_action.split(".")[0]
        #mimesis_class_name = self.mimesis_action.split(".")[1]
        # Import the class of the action based on its name and submodule 
        #submodule = importlib.import_module(f".{module_name}", actions.__name__)
        #ActionClass = getattr(submodule, mimesis_class_name)
        # Here is where we initialize the action with the parameters from the form
        #actionClass = ActionClass(**action_parameters)

        action = actions.Action.load_from_file(f"./library/{self.mimesis_action}")
        action.prompt.parameters = action_parameters

        if self.document_input:
            if instruction.project:
                if instruction.project.document:
                    document = instruction.project.document
                    action.prompt.parameters[self.document_input] = document.text

        # Load Agent from caché
        agent = Agent(**json.loads(request.session['agent']))

        # Execute action in mimesis
        logging.info(f"Calling Mimesis action {action.name}")
        reply = agent.do(action)

        instruction.finished = True
        instruction.save()

        return reply