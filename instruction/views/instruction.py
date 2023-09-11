import urllib

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect

from ..models import Instruction, InstructionElement, InstructionElementAgentCall, InstructionElementMessage, InstructionElementTextInput, MessageBlock
from ..forms import InstructionTypeCreateForm, InstructionUpdateForm
from projects.models import Project

class InstructionIndexView(View):

    def get(self, request, project_id=None):
        """Get all the instructions. If project is given limit to that project.
        """
        print("InstructionIndexView.get")
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            action = project.action
            instructions = Instruction.objects.filter(project=project_id)
            instructions_possible = Instruction.objects.filter(type__action=action, template=True, show_as_possible=True).exclude(type__in=instructions.values_list("type", flat=True))
        else:
            instructions = Instruction.objects.all()
            if request.GET.get("template"):
                instructions = instructions.filter(template=True)
            if request.GET.get("action"):
                instructions = instructions.filter(type__action=request.GET.get("action"))
                
            instructions_possible = None

        context = {
            "instructions": instructions,
            "instructions_possible": instructions_possible
        }
        return render(request, "instruction/instructions.html", context)

    @staticmethod
    def forward(response, project=None, **kwargs):
        print("InstructionIndexView.forward")
        get = kwargs.pop('get', {})
        if project:
            url = reverse("instruction:index", kwargs={"project_id":project.pk})
        else:
            url = reverse("instruction:index")
        if get:
            url += '?' + urllib.parse.urlencode(get)
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instructions' hidden></div>")
        print(response)
        return response

instruction_index_view = InstructionIndexView.as_view()

class InstructionCreateView(View):
    def post(self, request):
        form = InstructionTypeCreateForm(request.POST)
        if form.is_valid():
            instruction = form.save()
            return JsonResponse({"instruction_id": instruction.id})
        return JsonResponse({"status": "Not created"})

class InstructionReadView(View):

    def get(self, request, instruction_id):
        """Get specific instruction

        Args:
            request (HttpRequest): The request
            instruction_id (int): The id of the instruction
        """
        print("InstructionReadView.get")
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_type = instruction.type
        action = instruction_type.action
        agent = action.agent

        elements = list(InstructionElementAgentCall.objects.filter(instruction_type=instruction_type)) \
                + list(InstructionElementMessage.objects.filter(instruction_type=instruction_type)) \
                + list(InstructionElementTextInput.objects.filter(instruction_type=instruction_type))
        elements.sort(key=lambda x: x.index)
        print(elements)
        context = {
            "action": action
            ,"instruction": instruction
            ,"agent": agent
            ,"elements": elements
        }
        return render(request, "instruction/instruction.html", context)
    
    @staticmethod
    def forward(response, instruction):
        url = reverse("instruction:read", kwargs={"instruction_id":instruction.pk})
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instruction-{instruction.pk}' hidden></div>")
        return response

instruction_read_view = InstructionReadView.as_view()
    
class InstructionUpdateView(View):

    def post(self, request, instruction_id):

        instruction = get_object_or_404(Instruction, id=instruction_id)
        form = InstructionUpdateForm(request.POST, instance=instruction)
        form.save()

instruction_update_view = InstructionUpdateView.as_view()

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

class InstructionCreateFromTemplateView(View):

    def post(self, request, instruction_id):
        project = get_object_or_404(Project, id=request.POST["project_id"])
        instruction = get_object_or_404(Instruction, id=instruction_id)

        instruction.pk = None
        instruction._state.adding = True
        instruction.template = False
        instruction.project = project
        instruction.save()

        return redirect("instruction:index", project_id=project.pk)

class InstructionReadTemplateView(View):

    def get(self, request, instruction_id):
        
        instruction = get_object_or_404(Instruction, id=instruction_id)
        context = {
            "instruction": instruction
        }
        return render(request, "instruction/instruction_template.html", context)
    
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