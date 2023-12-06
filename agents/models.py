import logging

from django.db import models
from django.templatetags.static import static

class AgentType(models.Model):
    
    name = models.CharField(max_length=256)
    definition = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    short_title = models.CharField(max_length=512, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="agents", null=True, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.name} - {self.short_title}"

class Trait(models.Model):

    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    self_definition = models.CharField(max_length=512)

    def __str__(self):
        return self.name

class Personality(models.Model):
    
    name = models.CharField(max_length=256)
    traits = models.ManyToManyField(Trait, blank=True)

    def __str__(self):
        return self.name

class Agent(models.Model):
    
    type = models.ForeignKey(AgentType, on_delete=models.CASCADE)
    company = models.ManyToManyField("company.Company")
    name =  models.CharField(max_length=256, null=True, blank=True) # Fields are optional as they could deafult to type.
    definition = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_title = models.CharField(max_length=512, null=True, blank=True)
    object = models.JSONField(null=True, blank=True)
    personality = models.ForeignKey(Personality, null=True, blank=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="agents", null=True, blank=True)
    show_in_explorer = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}. {self.get_name} - {self.get_short_title}"
    
    def greeting_message(self):
        return "Hi! How can I help you?"

    def check_project(self, project):

        if project.action.name == "Feedback Advice":

            project.add_instruction("Feedback follow up")

            return True

    def prompt(self, prompt:str, prompt_parameters:dict = {}):
        from mimesis.agent.agent import Agent as AgentMimesis
        from mimesis.actions.actions import Action, ActionReply
        from mimesis.prompt.prompt import PromptTemplate
        mms_agent = AgentMimesis(name=self.get_name, definition=self.get_definition)
        reply = mms_agent.do(Action(
            name="prompt",
            description="",
            definition="",
            reply=ActionReply(type="Answer",name="Prompt reply"),
            prompt=PromptTemplate(text=prompt, parameters=prompt_parameters),
            memory=""
            ))
        logging.warning(reply)
        return reply

    def stream_prompt(self, request, prompt, fast=False):
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        # Group names are set to the view path, so that each view call answers to a specific socket group.
        group_name = request.path.replace("/", "")
        async_to_sync(channel_layer.group_send)(group_name, {"type": "llm.call", "prompt":prompt, "fast":fast})

    def do(self, action_file, action_parameters:dict = {}):
        from mimesis.agent.agent import Agent as AgentMimesis
        from mimesis.actions.actions import Action
        mms_agent = AgentMimesis(name=self.get_name, definition=self.get_definition)
        action = Action.load_from_file(action_file)
        action.prompt.parameters = action_parameters
        reply = mms_agent.do(action)
        return reply[0]

    @property
    def get_definition(self):
        if self.definition:
            return self.definition
        elif self.type.definition:
            return self.type.definition

    @property
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        elif self.type.profile_picture:
            return self.type.profile_picture.url
        else:
            return static('assets/images/profile.png')
    
    @property
    def get_short_title(self):
        if self.short_title:
            return self.short_title
        else:
            return self.type.short_title
        
    @property
    def get_name(self):
        if self.name:
            return self.name
        else:
            return self.type.name