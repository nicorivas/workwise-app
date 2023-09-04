from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, response, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect

from .forms import InstructionTypeCreateForm
from .models import Instruction, InstructionType, Message, MessageBlock
from action_element.forms import ActionElementCreateForm
from action_element.models import ActionElementAgentCall, ActionElementMessage, ActionElementTextInput
from projects.models import Project

class InstructionTypeCreateView(View):
    """Create a new InstructionType. This view is called from the action page, and it returns the id of the new InstructionType.

    This also creates a preview instruction, to be used in the action page.
    
    Returns:
        JsonResponse: The id of the new InstructionType.
    """
    def post(self, request):
        form = InstructionTypeCreateForm(request.POST)
        if form.is_valid():
            instruction_type = form.save()
            # We create a preview instruction to use in the action page
            instruction = Instruction(type=instruction_type, preview=True)
            instruction.save()
            return JsonResponse({"instruction_type_id": instruction_type.id})
        return JsonResponse({"status": "Not created"})

class InstructionTypeReadView(View):
    def get(self, request, instruction_type_id):
        instruction_type = get_object_or_404(InstructionType, id=instruction_type_id)
        action = instruction_type.action
        agent = action.agent
        action_element_create_form = ActionElementCreateForm()
        action_elements = list(ActionElementAgentCall.objects.filter(instruction_type=instruction_type)) \
            + list(ActionElementMessage.objects.filter(instruction_type=instruction_type)) \
            + list(ActionElementTextInput.objects.filter(instruction_type=instruction_type))
        action_elements.sort(key=lambda x: x.index)
        context = {
            "action": action
            ,"instruction_type": instruction_type
            ,"agent": agent
            ,"action_element_create_form": action_element_create_form
            ,"action_elements": action_elements
        }
        return render(request, "instruction/instruction_type.html", context)

class InstructionCreateView(View):
    def post(self, request):
        form = InstructionTypeCreateForm(request.POST)
        if form.is_valid():
            instruction = form.save()
            return JsonResponse({"instruction_id": instruction.id})
        return JsonResponse({"status": "Not created"})

class InstructionIndexView(View):

    def get(self, request, project_id=None):
        """Get all the instructions. If project is given limit to that project.
        """
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            action = project.action
            instructions = Instruction.objects.filter(project=project_id)
            instructions_possible = Instruction.objects.filter(type__action=action, preview=True, show_as_possible=True).exclude(type__in=instructions.values_list("type", flat=True))
        else:
            instructions = Instruction.objects.all()
            instructions_possible = None

        context = {
            "instructions": instructions,
            "instructions_possible": instructions_possible
        }
        return render(request, "instruction/instructions.html", context)

    @staticmethod
    def forward(response, project):
        url = reverse("instruction:index", kwargs={"project_id":project.pk})
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instructions' hidden></div>")
        return response

class InstructionReadView(View):

    def get(self, request, instruction_id):
        
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_type = instruction.type
        action = instruction_type.action
        agent = action.agent

        action_element_create_form = ActionElementCreateForm()
        elements = list(ActionElementAgentCall.objects.filter(instruction_type=instruction_type)) \
                + list(ActionElementMessage.objects.filter(instruction_type=instruction_type)) \
                + list(ActionElementTextInput.objects.filter(instruction_type=instruction_type))
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
    
class InstructionDeleteView(View):

    def delete(self, request, instruction_id):
        
        instruction = get_object_or_404(Instruction, id=instruction_id)
        project = instruction.project
        instruction.delete()
        if project:
            response = HttpResponse()
            response = InstructionIndexView.forward(response, project) # Refresh all instructions
            return response
        else:
            return HttpResponse('')
    
    @staticmethod
    def forward(response, instruction):
        url = reverse("instruction:read", kwargs={"instruction_id":instruction.pk})
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instruction-{instruction.pk}' hidden></div>")
        return response
    
class InstructionCreateFromPreviewView(View):

    def post(self, request, instruction_id):
        project = get_object_or_404(Project, id=request.POST["project_id"])
        instruction = get_object_or_404(Instruction, id=instruction_id)

        instruction.pk = None
        instruction._state.adding = True
        instruction.preview = False
        instruction.project = project
        instruction.save()

        return redirect("instruction:index", project_id=project.pk)

class InstructionReadPreviewView(View):

    def get(self, request, instruction_id):
        
        instruction = get_object_or_404(Instruction, id=instruction_id)
        context = {
            "instruction": instruction
        }
        return render(request, "instruction/instruction_preview.html", context)
    
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