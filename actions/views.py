import time
import logging
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from document.models import Document
from django.urls import reverse

from .models import ActionDB
from mimesis.agent.agent import Agent
from mimesis.actions.project import EvaluatePrompt, WriteProject, ReviseProject, ApplyRevision

from projects.models import Project, Message

# Create your views here.
class EvaluateProjectCharter(View):

    def post(self, request, action_id):
        print("EvaluateProjectCharter.post")

        # instruction = get_object_or_404(Instruction, id=instruction_id)
        # instruction.prompt = request.POST.get("prompt")
        # instruction.save()

        agent = Agent(**json.loads(request.session['agent']))
        action = EvaluatePrompt(project_description=instruction.prompt)
        reply = agent.do(action)
        project = get_object_or_404(Project, pk=project_id)
        agent = get_object_or_404(Project, pk=project_id)

        enough_information = json.loads(reply)["enough_information"]
        comments = json.loads(reply)["comments"]

        if enough_information:
            message_type = "status"
        else:
            message_type = "error"

        # Add message, that is the reply of the agent
        message = Message.objects.create(
            project=project,
            message=comments,
            agent=project.agent,
            instruction=instruction,
            user="Agent",
            type=message_type
            )
        message.save()

        context = {
            "instruction": instruction,
            "reply": reply,
        }
        return render(request, "projects/instruction.html", context)