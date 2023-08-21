from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, response
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .forms import InstructionTypeCreateForm
from .models import Instruction, InstructionType, Message, MessageBlock
from action_element.forms import ActionElementCreateForm
from action_element.models import ActionElementAgentCall, ActionElementMessage, ActionElementTextInput

class InstructionTypeReadView(View):
    def get(self, request, instruction_type_id):
        instruction_type = get_object_or_404(InstructionType, id=instruction_type_id)
        action = instruction_type.action
        agent = action.agent
        action_element_create_form = ActionElementCreateForm()
        elements = list(ActionElementAgentCall.objects.filter(action=action)) + list(ActionElementMessage.objects.filter(action=action)) + list(ActionElementTextInput.objects.filter(action=action))
        elements.sort(key=lambda x: x.index)
        context = {
            "action": action
            ,"instruction_type": instruction_type
            ,"agent": agent
            ,"action_element_create_form": action_element_create_form
            ,"elements": elements
        }
        return render(request, "instruction/instruction_type.html", context)

class InstructionCreateView(View):
    def post(self, request):
        form = InstructionTypeCreateForm(request.POST)
        if form.is_valid():
            instruction = form.save()
            return JsonResponse({"instruction_id": instruction.id})
        return JsonResponse({"status": "Not created"})

class InstructionReadView(View):

    def get(self, request, instruction_id):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        action = instruction.type.action
        agent = action.agent
        action_element_create_form = ActionElementCreateForm()
        elements = list(ActionElementAgentCall.objects.filter(action=action)) + list(ActionElementMessage.objects.filter(action=action)) + list(ActionElementTextInput.objects.filter(action=action))
        elements.sort(key=lambda x: x.index)
        context = {
            "action": action
            ,"instruction": instruction
            ,"agent": agent
            ,"action_element_create_form": action_element_create_form
            ,"elements": elements
        }
        return render(request, "instruction/instruction.html", context)
    
    @staticmethod
    def forward(response, instruction):
        url = reverse("instruction:read", kwargs={"instruction_id":instruction.pk})
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instruction-{instruction.pk}' hidden></div>")
        return response
    
class InstructionSelectMessageBlockView(View):

    def post(request, message_block_id):

        message_block = get_object_or_404(MessageBlock, id=message_block_id)
        message_block.selected = not message_block.selected
        message_block.save()

        return render(request, "instruction/message_block.html", {"block": message_block})