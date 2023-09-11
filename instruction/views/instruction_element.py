from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from ..forms import InstructionElementCreateForm, InstructionElementUpdateForm, InstructionElementMessageUpdateForm, InstructionElementAgentCallUpdateForm
from instruction.models import Instruction, InstructionType, InstructionElement, InstructionElementAgentCall, InstructionElementMessage, InstructionElementTextInput
# Forwards
from document.views import DocumentRefreshView
from instruction.views.instruction import InstructionReadView

class InstructionElementIndexView(View):
    def get(self, request, instruction_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_elements = list(InstructionElementAgentCall.objects.filter(instruction_type=instruction.type)) \
            + list(InstructionElementMessage.objects.filter(instruction_type=instruction.type)) \
            + list(InstructionElementTextInput.objects.filter(instruction_type=instruction.type))
        instruction_elements.sort(key=lambda x: x.index)
        context = {"instruction": instruction, "elements": instruction_elements, "agent": instruction.type.action.agent}
        return render(request, "instruction/elements/index.html", context)

instruction_element_index_view = InstructionElementIndexView.as_view()

class InstructionElementCreateView(View):

    def post(self, request, instruction_id:int):
        print("InstructionElementCreateView.post")
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_type = instruction.type
        form = InstructionElementCreateForm(request.POST)
        if form.is_valid():
            # We must define a case for each type of element, due to inheritance of classes.
            # We do not commit the first one as we want to save the correct instruction element.
            instruction_element = form.save(commit=False)
            if instruction_element.type.name == instruction_element.type.InstructionElementTypes.AGENT_CALL:
                agent_call = InstructionElementAgentCall(name=instruction_element.name, instruction_type=instruction_type)
                agent_call.save()
            elif instruction_element.type.name == instruction_element.type.InstructionElementTypes.MESSAGE:
                message = InstructionElementMessage(name=instruction_element.name, instruction_type=instruction_type)
                message.save()
            elif instruction_element.type.name == instruction_element.type.InstructionElementTypes.TEXT_INPUT:
                text_input = InstructionElementTextInput(name=instruction_element.name, instruction_type=instruction_type)
                text_input.save()
            
            return redirect("instruction:element_index", instruction_id=instruction.pk)

instruction_element_create_view = InstructionElementCreateView.as_view()

class InstructionElementReadView(View):

    def get(self, request, instruction_type_id:int, action_element_id:int):
        instruction_type = get_object_or_404(InstructionType, id=instruction_type_id)
        instruction_element = get_object_or_404(InstructionElement, id=action_element_id)
        if action_element.type.name == action_element.type.InstructionElementTypes.AGENT_CALL:
            action_element = get_object_or_404(InstructionElementAgentCall, id=action_element_id)
            form = InstructionElementAgentCallUpdateForm(instance=action_element)
        else:
            form = InstructionElementUpdateForm(instance=action_element)
        return render(request, "action_element/update_form.html", {"instruction_type": instruction_type, "element":action_element, "form": form})

class InstructionElementUpdateView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        print("InstructionElementUpdateView.post")
        print(request.POST)
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element = get_object_or_404(InstructionElement, id=instruction_element_id)
        instruction_element_form = InstructionElementUpdateForm(request.POST, instance=instruction_element)
        if instruction_element_form.is_valid():
            instruction_element_form.save()

        if instruction_element.type.name == instruction_element.type.InstructionElementTypes.MESSAGE:
            message = get_object_or_404(InstructionElementMessage, id=instruction_element_id)
            message_form = InstructionElementMessageUpdateForm(request.POST, instance=message)
            if message_form.is_valid():
                message_form.save()
                instruction_element.save()
                return HttpResponse('')

        return HttpResponse('')
        #return redirect("actions:read", action_id=instruction_type.action.pk)

instruction_element_update_view = InstructionElementUpdateView.as_view()

class InstructionElementDeleteView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        print("InstructionElementDeleteView.post")
        action_element = get_object_or_404(InstructionElement, id=instruction_element_id)
        action_element.delete()
        return HttpResponse('')

instruction_element_delete_view = InstructionElementDeleteView.as_view()

class InstructionElementCallView(View):

    def post(self, request, instruction_id:int, action_element_id:int):
        """Triggered by call elements on push of button.

        Main idea here is to call the agent and update what is necessary after the agent call.
        Agent is called on model of the InstructionElementAgentCall(InstructionElement).

        Args:
            request (HttpRequest): Request object
            instruction_id (int): Instruction id
            action_element_id (int): Action element id
        """

        print("ElementCallView.post")

        response = HttpResponse()

        instruction = get_object_or_404(Instruction, id=instruction_id)
        agent_call = get_object_or_404(InstructionElementAgentCall, id=action_element_id)
        replies = agent_call.call_agent(request, instruction)
        if instruction.project:
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
            response = DocumentRefreshView.forward(response, document) # Refresh the document
            response = InstructionReadView.forward(response, instruction) # Refresh the instruction

        return response