import json
from django.shortcuts import render, get_object_or_404
from django.views import View

from agents.models import Agent
from .models import Action
from mimesis.actions.project import EvaluatePrompt, WriteProject, ReviseProject, ApplyRevision
from django.views.decorators.csrf import csrf_exempt

from instruction.models import InstructionElement, InstructionElementAgentCall, InstructionElementMessage, InstructionElementTextInput
from instruction.forms import InstructionElementCreateForm
from instruction.forms import InstructionTypeCreateForm
from instruction.models.instruction import Instruction

class ActionsView(View):

    def get(self, request, action_id=None):
        print("ActionsView.get")
        # Get all actions
        actions = Action.objects.all()
        if action_id:
            action = get_object_or_404(Action, id=action_id)
        else:
            action = actions.first()
        context = {
            "actions": actions,
            "action": action
        }
        return render(request, "actions/index.html", context)

class ActionReadView(View):

    def get(self, request, action_id):
        print("ActionReadView.get")
        actions = Action.objects.all()
        agent = get_object_or_404(Agent, id=1)
        action = get_object_or_404(Action, id=action_id)
        instruction_element_create_form = InstructionElementCreateForm()
        elements = list(InstructionElementAgentCall.objects.filter(instruction_type__action=action)) \
            + list(InstructionElementMessage.objects.filter(instruction_type__action=action)) \
            + list(InstructionElementTextInput.objects.filter(instruction_type__action=action))
        elements.sort(key=lambda x: x.index)
        context = {
            "actions": actions
            ,"action": action
            ,"agent": agent
            ,"elements": elements
            ,"action_element_create_form": instruction_element_create_form
        }
        return render(request, "actions/actions.html", context)
    
class ActionReadInstructionTypesView(View):

    def get(self, request, action_id):
        print("ActionReadInstructionTypesView.get")
        agent = get_object_or_404(Agent, id=1)
        action = get_object_or_404(Action, id=action_id)
        form = InstructionTypeCreateForm()
        instructions = Instruction.objects.filter(type__action=action, template=True)
        print(instructions)
        context = {
            "action": action
            ,"agent": agent
            ,"form": form
            ,"instructions": instructions
        }
        return render(request, "actions/instruction_types.html", context)
    
class ActionInstructionsCreateView(View):

    def post(self, request, action_id):
        print("ActionInstructionsCreateView.get")
        agent = get_object_or_404(Agent, id=1)
        action = get_object_or_404(Action, id=action_id)
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
        agent = get_object_or_404(Agent, id=1)
        action = get_object_or_404(Action, id=action_id)
        action.call_agent(request)
        return render(request, "actions/action.html", {})