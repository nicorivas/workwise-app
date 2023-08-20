from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .forms import ActionElementCreateForm, ActionElementUpdateForm, AgentCallUpdateForm
from .models import ActionElement, ActionElementAgentCall, ActionElementMessage, ActionElementTextInput
from actions.models import Action

class ElementCreateView(View):

    def post(self, request, action_id:int):
        action = get_object_or_404(Action, id=action_id)
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

    def get(self, request, action_id:int, action_element_id:int):
        action = get_object_or_404(Action, id=action_id)
        action_element = get_object_or_404(ActionElement, id=action_element_id)
        if action_element.type.name == action_element.type.ActionElementTypes.AGENT_CALL:
            action_element = get_object_or_404(ActionElementAgentCall, id=action_element_id)
            form = AgentCallUpdateForm(instance=action_element)
        else:
            form = ActionElementUpdateForm(instance=action_element)
        return render(request, "action_element/update_form.html", {"action": action, "element":action_element, "form": form})

class ElementUpdateView(View):

    def post(self, request, action_id:int, action_element_id:int):
        print("ElementUpdateView.post")

        action = get_object_or_404(Action, id=action_id)
        action_element = get_object_or_404(ActionElement, id=action_element_id)
        form = ActionElementUpdateForm(request.POST, instance=action_element)
        if form.is_valid():
            print("1")
            form.save()
            if action_element.type.name == action_element.type.ActionElementTypes.AGENT_CALL:
                agent_call = get_object_or_404(ActionElementAgentCall, id=action_element_id)
                print("agent_call: ", agent_call)
                agent_call_form = AgentCallUpdateForm(request.POST, instance=agent_call)
                print("agent_call_form: ", agent_call_form)
                if agent_call_form.is_valid():
                    print("2")
                    agent_call_form.save()

        return redirect("actions:action", action_id=action_id)

class ElementDeleteView(View):

    def post(self, request, action_id:int):
        action_element_id = request.POST.get("action_element_id")
        action_element = get_object_or_404(ActionElement, id=action_element_id)
        action_element.delete()
        return redirect("actions:action", action_id=action_id)

class ElementCallView(View):

    def post(self, request, action_id:int, action_element_id:int):
        
        agent_call = get_object_or_404(ActionElementAgentCall, id=action_element_id)
        reply = agent_call.call_agent(request)
        print(reply)
        return redirect("actions:action", action_id=action_id)