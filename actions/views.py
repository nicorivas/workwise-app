import json
from django.shortcuts import render, get_object_or_404
from django.views import View

from agents.models import AgentDB
from .models import Action
#from mimesis.agent.agent import Agent
from mimesis.actions.project import EvaluatePrompt, WriteProject, ReviseProject, ApplyRevision
from django.views.decorators.csrf import csrf_exempt

from action_element.models import ActionElement, ActionElementAgentCall, ActionElementMessage, ActionElementTextInput
from action_element.forms import ActionElementCreateForm
from instruction.forms import InstructionTypeCreateForm
from instruction.views import InstructionCreateView

class ActionsView(View):

    def get(self, request):
        print("ActionsView.get")
        # Get all actions
        actions = Action.objects.all()
        context = {
            "actions": actions
        }
        return render(request, "actions/index.html", context)

class ActionReadView(View):

    def get(self, request, action_id):
        print("ActionReadView.get")
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
    
class ActionReadInstructionTypesView(View):

    def get(self, request, action_id):
        print("ActionReadInstructionTypesView.get")
        agent = get_object_or_404(AgentDB, id=1)
        action = get_object_or_404(Action, id=action_id)
        form = InstructionTypeCreateForm()
        context = {
            "action": action
            ,"agent": agent
            ,"form": form
        }
        return render(request, "actions/instruction_types.html", context)
    
class ActionInstructionsCreateView(View):

    def post(self, request, action_id):
        print("ActionInstructionsCreateView.get")
        agent = get_object_or_404(AgentDB, id=1)
        action = get_object_or_404(Action, id=action_id)
        instruction = InstructionCreateView.as_view()(request)
        form = InstructionTypeCreateForm()
        context = {
            "action": action
            ,"agent": agent
            ,"form": form
        }
        return render(request, "actions/instructions.html", context)

class ActionCallView(View):

    def get(self, request, action_id):
        print("ActionView.get")
        agent = get_object_or_404(AgentDB, id=1)
        action = get_object_or_404(Action, id=action_id)
        action.call_agent(request)
        return render(request, "actions/action.html", {})