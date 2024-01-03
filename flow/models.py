import json, logging

from django.db import models
from django.shortcuts import get_object_or_404

from mimesis.actions import actions
from mimesis.agent import agent as agentMimesis

from instruction.models import InstructionType
from agents.models import Agent
from company.models import Company
from projects.models import Project
from actions.models import Action

# Flow model
class Flow(models.Model):
    name = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    logo = models.ImageField(upload_to="flow_logos", null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    footer_text = models.TextField(default="", null=True, blank=True)
    register = models.BooleanField(default=False)
    debug = models.BooleanField(default=False)
    style = models.CharField(max_length=32, choices=[("default", "Default"), ("web", "Web")], default="default")
    css = models.CharField(max_length=64, default="flow.css")
    instruction_types = models.ManyToManyField(InstructionType, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"

# Create a Pitch model
class Pitch(models.Model):

    STARTUP_LEVEL = [
        ("1", "Idea"),
        ("2", "Prototipo"),
        ("3", "Constituido"),
        ("4", "Escalamiento"),
    ]

    author_name = models.CharField(max_length=256)
    author_email = models.EmailField()
    startup_name = models.CharField(max_length=256)
    startup_level = models.CharField(max_length=1, choices=STARTUP_LEVEL, default="1")
    pitch = models.TextField(default="")
    pitch_prompt = models.TextField(default="")
    pitch_analysis_short = models.TextField(default="")
    pitch_analysis_long = models.TextField(default="")