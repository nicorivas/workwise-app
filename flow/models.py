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
    debug = models.BooleanField(default=False)
    instruction_types = models.ManyToManyField(InstructionType, blank=True)

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

    def analyse(self, request):
        agent = get_object_or_404(Agent, pk=1)
        mimesis_action = "mimesis/library/pitch_evaluation/PitchEvaluation"
        action = actions.Action.load_from_file(f"{mimesis_action}")
        agent_mimesis = agentMimesis.Agent()
        prompt = action.do(agent_mimesis, pitch=request.POST["query"])
        agent.stream_prompt(request, prompt, fast=False)

    def analyse_long(self, request):
        agent = get_object_or_404(Agent, pk=1)
        mimesis_action = "mimesis/library/pitch_evaluation/PitchEvaluationLong"
        action = actions.Action.load_from_file(f"{mimesis_action}")
        agent_mimesis = agentMimesis.Agent()
        prompt = action.do(agent_mimesis, pitch=request.POST["pitch"])
        response = agent.prompt(prompt, {"pitch":request.POST["pitch"]})
        self.pitch_analysis_long = response[0]["text"]
        self.save()