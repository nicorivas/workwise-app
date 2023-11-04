import json, logging

from django.db import models
from django.utils.translation import gettext_lazy as _
from .instruction import InstructionType, Message

from document.models import Document
from mimesis.agent.agent import Agent
import mimesis.actions.actions as actions

class InstructionElementType(models.Model):

    class InstructionElementTypes(models.TextChoices):
        MESSAGE = "MSG", _("Message")
        CHOICES = "CHO", _("Choices")
        TEXT_INPUT = "TXT", _("Text Input")
        AGENT_CALL = "ACA", _("Agent Call")
        REVISE = "RVS", _("Revise")
        REVISION = "REV", _("Revision")
        DOCUMENT_LINK = "DOC", _("Document")

    name = models.CharField(max_length=3, choices=InstructionElementTypes.choices, default=InstructionElementTypes.MESSAGE)
    description = models.TextField()

    def __str__(self):
        return self.name

    def template(self):
        if self.name == self.InstructionElementTypes.MESSAGE:
            return "instruction/elements/message.html"
        elif self.name == self.InstructionElementTypes.TEXT_INPUT:
            return "instruction/elements/text_input.html"
        elif self.name == self.InstructionElementTypes.AGENT_CALL:
            return "instruction/elements/agent_call.html"
        elif self.name == self.InstructionElementTypes.DOCUMENT_LINK:
            return "instruction/elements/document_link.html"
        elif self.name == self.InstructionElementTypes.REVISE:
            return "instruction/elements/revise.html"
        elif self.name == self.InstructionElementTypes.REVISION:
            return "instruction/elements/revision.html"
        elif self.name == self.InstructionElementTypes.CHOICES:
            return "instruction/elements/choices.html"

    @property
    def label(self):
        return self.get_name_display() 
    
    @staticmethod
    def get_types():
        return InstructionElementType.InstructionElementTypes.choices

class InstructionElement(models.Model):
    """An instruction element is an element of an instruction, which constructs actions.

    It is an abstract element, think of it as a form element.

    Attributes:
        instruction_type (InstructionType): The instruction type that the element belongs to.
        index (int): The index of the element in the instruction type.
        type (InstructionElementType): The type of the element.
        name (str): The name of the element.
        guide (str): The guide of the element.
    """

    type = models.ForeignKey(InstructionElementType, on_delete=models.CASCADE)
    instruction_type = models.ForeignKey(InstructionType, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    index = models.IntegerField(default=0)
    guide = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.instruction_type.name} - {self.type} - {self.name}"
    
    def template(self):
        return self.type.template()
    
    def get_types(self):
        return InstructionElementType.InstructionElementTypes.choices
    
    @property
    def name_for_html(self):
        # Conver self title to a string that can be used as an id in html.
        if self.name == None:
            return ""
        elif isinstance(self.name, str):
            return self.name.replace(" ", "_").replace(".", "_").replace(",", "_").replace(":", "_").replace(";", "_").replace("?", "_").replace("!", "_").replace("(", "_").replace(")", "_").replace("[", "_").replace("]", "_").replace("{", "_").replace("}", "_").replace("/", "_").replace("\\", "_").replace("'", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("=", "_").replace("+", "_").replace("-", "_").replace("*", "_").replace("&", "_").replace("^", "_").replace("%", "_").replace("$", "_").replace("#", "_").replace("@", "_").lower()
        else:
            return self.name    
    

class InstructionElementTextInput(InstructionElement):

    message = models.TextField(null=True, blank=True)
    audio = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = InstructionElementType.objects.get(name=InstructionElementType.InstructionElementTypes.TEXT_INPUT)

    def __str__(self):
        return self.name
    
    def template(self):
        return self.type.template()

class InstructionElementMessage(InstructionElement):

    message = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = InstructionElementType.objects.get(name=InstructionElementType.InstructionElementTypes.MESSAGE)

    def __str__(self):
        return self.name
    
    def template(self):
        return self.type.template()

class InstructionElementAgentCall(InstructionElement):

    button_label = models.CharField(max_length=256, default="Submit")
    mimesis_action = models.CharField(max_length=256, null=True, blank=True)
    document_input = models.CharField(max_length=256, null=True, blank=True)
    working_message = models.CharField(max_length=256, null=True, blank=True)
    stream = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = InstructionElementType.objects.get(name=InstructionElementType.InstructionElementTypes.AGENT_CALL)

    def __str__(self):
        return self.name
    
    def call_agent(self, request, instruction, stream=False):
        print(f"InstructionElementAgentCall.call_agent() called: {request.POST}")

        # Update instruction data based on POST, that is, the form values
        instruction.update(request.POST)

        # The parameters to give to the agent action are held in the instruction data, that is, the values of the form.
        action_parameters = instruction.data

        # Load action from file description in Mimesis library
        action = actions.Action.load_from_file(f"{self.mimesis_action}")

        # Set parameters of action to data of the instruction
        action.prompt.parameters = action_parameters

        # Add document text to prompt parameters
        if self.document_input:
            if instruction.task:
                if instruction.task.get_active_document(format=False):
                    document = instruction.task.get_active_document(format=False)
                    action.prompt.parameters[self.document_input] = document.text

        # Add linked documents. Link documents are sent to the back by id, so we need to retrieve the text of the document.
        document_links = InstructionElementDocumentLink.objects.filter(instruction_type=instruction.type)
        for document_link in document_links:
            action.prompt.parameters[document_link.name] = Document.objects.get(pk=action_parameters[document_link.name]).text

        print(action.prompt.parameters)

        replies = []

        if False:
            for element in document.get_elements():
                action.prompt.parameters["section"] = element.title

                print(action.prompt.parameters)
                print(action.prompt.get_prompt())

                # Load Agent from caché
                agent = Agent(**json.loads(request.session['agent']))

                # Execute action in mimesis
                logging.info(f"Calling Mimesis action {action.name}")
                reply = agent.do(action)
                replies += reply

                instruction.finished = True
                instruction.save()
        else:
            
            # Load Agent from caché
            agent = Agent(**json.loads(request.session['agent']))

            if not stream:
                # In the syncrhonous case (we wait until LLM response is finished), just execute action in mimesis
                print(f"Calling Mimesis action {action.name}")
                print(f"{action.prompt.get_prompt()}")
                reply = agent.do(action)
                replies += reply
                instruction.finished = True
                instruction.save()
                return replies
            else:
                # In the asynchronous case (we stream LLM response), we return the prompt to the front to make the async request.
                print(f"Getting prompt from Mimesis {action.name}")
                prompt = agent.prompt(action=action)
                self.instruction_type.action.agent.stream_prompt(request, prompt, fast=False)
                return prompt

        return replies

class InstructionElementRevise(InstructionElement):
    """
    Element used to trigger revision of a document.
    It creates one or more InstructionElementRevision elements.
    When InstructionElementRevision elements are created, they call the agent.

    Attributes:
        button_label (str): The label of the button.
        by_section (bool): If True, the revision is done by section. If False, the revision is done by document.
    """
    
    button_label = models.CharField(max_length=256, default="Submit")
    by_section = models.BooleanField(default=True)

    def call(self, request, instruction):
        print("InstructionElementRevise.call", request.POST)

        document = instruction.task.get_active_document()
        # Clear document elements and create them from json
        document.clear_elements()
        document.create_elements_from_json()

        if self.by_section:
            elements = document.get_elements(sorted=True)
            for i, element in enumerate(elements):
                instruction_element_revision = InstructionElementRevision.objects.create(
                    instruction_type=self.instruction_type,
                    index=100+i,
                    name=f"{element.title}",
                    mimesis_action="./mimesis/library/project_charter/ReviseProjectCharterSection",
                    document=document,
                    document_element=element
                )
                instruction_element_revision.save()
                instruction_element_revision.call_agent(request, instruction)
                if i == 3: break
        else:
            instruction_element_revision = InstructionElementRevision.objects.create(
                instruction_type=self.instruction.type,
                index=self.index,
                name=f"Revise {document.name}",
                guide=f"Revise {document.name}",
                mimesis_action="./mimesis/library/project_charter/ReviseProjectCharter",
                document=document,
                document_element=None
            )
            instruction_element_revision.save()
            instruction_element_revision.call_agent(request)
        
        return True


class InstructionElementRevision(InstructionElement):
    """
    Element used to call the agent to revise a document.
    They are created by the InstructionElementRevise button.
    By default the agent is called automatically on creation of the element.
    It exists as we want to be able to produce parallel calls of revision.
    They are related one to one with a section of the document.
    """

    # The message that is created when the agent is called
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    # If the agent was called
    was_revised = models.BooleanField(default=False)
    # The action that is called
    mimesis_action = models.CharField(max_length=256, null=True, blank=True)
    # The document that is being revised
    document = models.ForeignKey("document.Document", on_delete=models.CASCADE, null=True, blank=True)
    # The index of the section of the document being revised
    document_section_index = models.IntegerField(null=True, blank=True)

    def call_agent(self, request, instruction):
        print("InstructionElementRevision.call_agent", request, instruction)

        action = actions.Action.load_from_file(f"{self.mimesis_action}")

        document_section_title = self.document.get_section_title(self.document_section_index)

        action.prompt.parameters["section"] = document_section_title
        action.prompt.parameters["project_charter"] = self.document.text

        # Call action on agent
        agent = Agent(**json.loads(request.session['agent']))
        reply = agent.do(action)

        print(reply)

        # Create of clear message, and set text
        if self.message:
            self.message.clear_blocks()
        else:
            self.message = Message.objects.create(instruction=instruction, title=document_section_title)
        self.message.set_text(reply[0]["text"], split_on=[("#", "Section")])
        self.was_revised = True
        self.save()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = InstructionElementType.objects.get(name=InstructionElementType.InstructionElementTypes.REVISION)

class InstructionElementDocumentLink(InstructionElement):

    document = models.ForeignKey("document.Document", on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=256, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = InstructionElementType.objects.get(name=InstructionElementType.InstructionElementTypes.DOCUMENT_LINK)

class InstructionElementChoices(InstructionElement):

    choices = models.JSONField(null=True, blank=True)
    style = models.CharField(max_length=256, null=True, blank=True,
                             choices=[
                                 ("radio", "Radio"),
                                 ("checkbox", "Checkbox"),
                                 ("select", "Select"),
                                 ("chips", "Chips")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = InstructionElementType.objects.get(name=InstructionElementType.InstructionElementTypes.CHOICES)

    def template(self):
        if self.style == "chips":
            return "instruction/elements/chips.html"
        else:
            return "instruction/elements/choices.html"

    def get_choices(self):
        return self.choices