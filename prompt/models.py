import logging

from jinja2 import Environment, BaseLoader, select_autoescape

from django.db import models
from actions.models import Action
from django.contrib.auth.models import User

class Prompt(models.Model):
    name = models.CharField(max_length=256)
    index = models.IntegerField(default=0)
    prompt = models.JSONField(default=dict)
    action = models.ManyToManyField(Action, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_updated_by')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"
    
    def get_prompt(self, parameters:dict = {}) -> str:
        template = Environment(loader=BaseLoader()).from_string(self.prompt["prompt"])
        prompt = template.render(self.parameters if parameters == {} else parameters)
        return prompt

    def call(self, group, parameters, stream=False, fast=False):
        # Group names are set to the view path, so that each view call answers to a specific socket group.
        if stream:
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer
            logging.warning(f"Prompt.stream_prompt {parameters}")

            prompt = self.get_prompt(parameters)
            logging.warning(f"Prompt.stream_prompt {prompt}")

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(group, {"type": "llm.call", "prompt":prompt, "fast":fast})
        else:
            return f"Call {self.name}"