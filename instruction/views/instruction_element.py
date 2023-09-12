from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from ..forms import InstructionElementCreateForm, InstructionElementUpdateForm, InstructionElementMessageUpdateForm, InstructionElementTextInputUpdateForm, InstructionElementAgentCallUpdateForm
from instruction.models import Instruction, InstructionType, InstructionElement, InstructionElementAgentCall, InstructionElementMessage, InstructionElementTextInput
# Forwards
from document.views import DocumentRefreshView
from instruction.views.instruction import InstructionReadView

def get_element_and_form(element, instance=False, request=None):

    if element.type.name == element.type.InstructionElementTypes.MESSAGE:
        element = get_object_or_404(InstructionElementMessage, id=element.pk)
    elif element.type.name == element.type.InstructionElementTypes.TEXT_INPUT:
        element = get_object_or_404(InstructionElementTextInput, id=element.pk)    
    elif element.type.name == element.type.InstructionElementTypes.AGENT_CALL:
        element = get_object_or_404(InstructionElementAgentCall, id=element.pk)

    form_args = []
    if request:
        form_args += [request.POST]
    
    form_kwargs = {}
    if instance:
        form_kwargs = {"instance": element}

    if element.type.name == element.type.InstructionElementTypes.MESSAGE:
        form = InstructionElementMessageUpdateForm(*form_args, **form_kwargs)
    elif element.type.name == element.type.InstructionElementTypes.TEXT_INPUT:
        form = InstructionElementTextInputUpdateForm(*form_args, **form_kwargs)
    elif element.type.name == element.type.InstructionElementTypes.AGENT_CALL:
        form = InstructionElementAgentCallUpdateForm(*form_args, **form_kwargs)
    
    return element, form

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

    def get(self, request, instruction_id:int, instruction_element_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element = get_object_or_404(InstructionElement, id=instruction_element_id)

        instruction_element, form = get_element_and_form(instruction_element, instance=False)

        return render(request, "instruction/elements/element.html", {"instruction": instruction, "element":instruction_element})

instruction_element_read_view = InstructionElementReadView.as_view()

class InstructionElementUpdateView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        print("InstructionElementUpdateView.post")
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element = get_object_or_404(InstructionElement, id=instruction_element_id)
        instruction_element_form = InstructionElementUpdateForm(request.POST, instance=instruction_element)
        if instruction_element_form.is_valid():
            instruction_element_form.save()


        instruction_element, form = get_element_and_form(instruction_element, instance=True, request=request)
        if form.is_valid():
            form.save()
            return redirect("instruction:element_read", instruction_id=instruction.pk, instruction_element_id=instruction_element.pk)

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

class InstructionElementDetailsView(View):

    def get(self, request, instruction_id:int, instruction_element_id: int):
        print("InstructionElementDetailsView.get")
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element = get_object_or_404(InstructionElement, id=instruction_element_id)
        instruction_element, form = get_element_and_form(instruction_element, instance=True)
        context = {"instruction": instruction, "element": instruction_element, "form": form}
        return render(request, 'instruction/elements/details.html', context)

instruction_element_details_view = InstructionElementDetailsView.as_view()

class InstructionElementCallView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        """Triggered by call elements on push of button.

        Main idea here is to call the agent and update what is necessary after the agent call.
        Agent is called on model of the InstructionElementAgentCall(InstructionElement).

        Args:
            request (HttpRequest): Request object
            instruction_id (int): Instruction id
            action_element_id (int): Action element id
        """

        print("InstructionElementCallView.post")

        response = HttpResponse()

        instruction = get_object_or_404(Instruction, id=instruction_id)
        agent_call = get_object_or_404(InstructionElementAgentCall, id=instruction_element_id)
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

instruction_element_call_view = InstructionElementCallView.as_view()