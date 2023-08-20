import json
from django.shortcuts import render, get_object_or_404
from django.views import View

from agents.models import AgentDB
from .models import Action
#from mimesis.agent.agent import Agent
from mimesis.actions.project import EvaluatePrompt, WriteProject, ReviseProject, ApplyRevision
from django.views.decorators.csrf import csrf_exempt

from projects.models import Project, Message
from action_element.models import ActionElement, ActionElementAgentCall, ActionElementMessage, ActionElementTextInput
from action_element.forms import ActionElementCreateForm

class ActionsView(View):

    def get(self, request):
        print("ActionsView.get")
        # Get all actions
        actions = Action.objects.all()
        context = {
            "actions": actions
        }
        return render(request, "actions/index.html", context)

class ActionView(View):

    def get(self, request, action_id):
        print("ActionView.get")
        agent = get_object_or_404(AgentDB, id=1)
        action = get_object_or_404(Action, id=action_id)
        action_element_create_form = ActionElementCreateForm()
        elements = list(ActionElementAgentCall.objects.filter(action=action)) + list(ActionElementMessage.objects.filter(action=action)) + list(ActionElementTextInput.objects.filter(action=action))
        elements.sort(key=lambda x: x.index)
        context = {
            "action": action
            ,"agent": agent
            ,"elements": elements
            ,"action_element_create_form": action_element_create_form
        }
        return render(request, "actions/action.html", context)

class ActionCallView(View):

    def get(self, request, action_id):
        print("ActionView.get")
        agent = get_object_or_404(AgentDB, id=1)
        action = get_object_or_404(Action, id=action_id)
        action.call_agent(request)
        return render(request, "actions/action.html", {})

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