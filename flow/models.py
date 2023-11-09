import json

from django.db import models
from django.shortcuts import get_object_or_404

from mimesis.actions import actions
from mimesis.agent import agent as agentMimesis

from agents.models import Agent

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
    
        prompt = action.do(agent_mimesis)

        agent.stream_prompt(request, prompt, fast=True)

        self.pitch_analysis_short = "Hola"