from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from .forms import ActionElementCreateForm, ActionElementUpdateForm, AgentCallUpdateForm
from .models import ActionElement, ActionElementAgentCall, ActionElementMessage, ActionElementTextInput
from instruction.models import Instruction
# Forwards
from document.views import DocumentRefreshView
from instruction.views import InstructionReadView

class ElementCreateView(View):

    def post(self, request, instruction_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        form = ActionElementCreateForm(request.POST)
        if form.is_valid():
            action_element = form.save(commit=False)

            if action_element.type.name == action_element.type.ActionElementTypes.AGENT_CALL:
                agent_call = ActionElementAgentCall(name=action_element.name, action=action)
                agent_call.save()
            elif action_element.type.name == action_element.type.ActionElementTypes.MESSAGE:
                message = ActionElementMessage(name=action_element.name, action=action)
                message.save()
            elif action_element.type.name == action_element.type.ActionElementTypes.TEXT_INPUT:
                text_input = ActionElementTextInput(name=action_element.name, action=action)
                text_input.save()
            
            return redirect("actions:action", action_id=action_id)

class ElementReadView(View):

    def get(self, request, instruction_id:int, action_element_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        action_element = get_object_or_404(ActionElement, id=action_element_id)
        if action_element.type.name == action_element.type.ActionElementTypes.AGENT_CALL:
            action_element = get_object_or_404(ActionElementAgentCall, id=action_element_id)
            form = AgentCallUpdateForm(instance=action_element)
        else:
            form = ActionElementUpdateForm(instance=action_element)
        return render(request, "action_element/update_form.html", {"action": action, "element":action_element, "form": form})

class ElementUpdateView(View):

    def post(self, request, instruction_id:int, action_element_id:int):
        print("ElementUpdateView.post")

        instruction = get_object_or_404(Instruction, id=instruction_id)
        action_element = get_object_or_404(ActionElement, id=action_element_id)
        form = ActionElementUpdateForm(request.POST, instance=action_element)
        if form.is_valid():
            form.save()
            if action_element.type.name == action_element.type.ActionElementTypes.AGENT_CALL:
                agent_call = get_object_or_404(ActionElementAgentCall, id=action_element_id)
                agent_call_form = AgentCallUpdateForm(request.POST, instance=agent_call)
                if agent_call_form.is_valid():
                    agent_call_form.save()

        return redirect("actions:action", action_id=action_id)

class ElementDeleteView(View):

    def post(self, request, action_id:int):
        action_element_id = request.POST.get("action_element_id")
        action_element = get_object_or_404(ActionElement, id=action_element_id)
        action_element.delete()
        return redirect("actions:action", action_id=action_id)

class ElementCallView(View):

    def post(self, request, instruction_id:int, action_element_id:int):
        """Triggered by call elements on push of button.

        Main idea here is to call the agent and update what is necessary after the agent call.
        Agent is called on model of the ActionElementAgentCall(ActionElement).

        Args:
            request (HttpRequest): Request object
            instruction_id (int): Instruction id
            action_element_id (int): Action element id
        """

        print("ElementCallView.post")

        instruction = get_object_or_404(Instruction, id=instruction_id)
        agent_call = get_object_or_404(ActionElementAgentCall, id=action_element_id)
        replies = agent_call.call_agent(request)
        for reply in replies:
            if reply["type"] == "document":
                document = instruction.project.document
                document.clear()
                document.text = reply["text"]
                document.create_element_from_reply(markdown=True)
                document.save()
            if reply["type"] == "message":
                instruction.delete_messages()
                instruction.add_message(reply["text"])
                pass

        
        # Forwards
        response = HttpResponse()
        response = DocumentRefreshView.forward(response, document) # Refresh the document
        response = InstructionReadView.forward(response, instruction) # Refresh the instruction

        return response