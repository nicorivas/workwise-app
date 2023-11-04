import urllib

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect

from ..models import Instruction, InstructionElement, InstructionElementType, InstructionElementDocumentLink, InstructionElementAgentCall, InstructionElementMessage, InstructionElementRevise, InstructionElementTextInput, Message, MessageBlock
from ..forms import InstructionTypeCreateForm, InstructionUpdateForm
from projects.models import Project
from task.models import Task

class MessageCallView(View):

    def post(self, request, message_id):
        print("MessageCallView.post")
        message = get_object_or_404(Message, id=message_id)
        reply = message.call_agent(request)
        return render(request, "instruction/message_blocks.html", {"message":message})
    
message_call_view = MessageCallView.as_view()

class InstructionIndexView(View):

    @staticmethod
    def get_instructions_context(task_id=None, edit=False, template=False):
        """Get all the instructions.
        
        If task is given, filter by that task.

        Args:
            ?task (int): The id of the task
            ?edit (bool): Whether to show edit buttons or not
            ?template (bool): Whether to show only templates
        """

        instructions = Instruction.objects.all()
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            action_id = task.action.id

        # If this is project view, then get possible instructions.
        instructions_possible = instructions.filter(type__action=action_id).filter(template=True)

        # Templates or not
        instructions = instructions.filter(template=template)

        # Filter by task
        if task_id:
            instructions = instructions.filter(task=task_id)

        # Remove from possible instructions those that the types are already in the created instructions
        instructions_possible = instructions_possible.exclude(type__id__in=instructions.values_list("type__id", flat=True))

        context = {
            "instructions": instructions
            ,"instructions_possible": instructions_possible
            ,"edit": edit
        }

        return context

    def get(self, request):
        """Get"""
        print("InstructionIndexView.get", request.GET)

        project_id = request.GET.get("project")
        action_id = request.GET.get("action")
        # If this is an edit view (as in Actions panel) or not (as in Project view)
        edit = "edit" in request.GET
        # If this is a template view (as in Actions panel) or not (as in Project view)
        template = "template" in request.GET

        context = self.get_instructions_context(project_id, action_id, edit, template)
        
        return render(request, "instruction/instructions.html", context)

    @staticmethod
    def forward(response, project=None, **kwargs):
        print("InstructionIndexView.forward")
        get = kwargs.pop('get', {})
        url = reverse("instruction:index")
        if get:
            url += '?' + urllib.parse.urlencode(get)
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instructions' hidden></div>")
        return response

instruction_index_view = InstructionIndexView.as_view()

class InstructionCreateView(View):
    def post(self, request):
        print("InstructionCreateView.post")
        form = InstructionTypeCreateForm(request.POST)
        if form.is_valid():
            instruction = form.save()
            return JsonResponse({"instruction_id": instruction.id})
        return JsonResponse({"status": "Not created"})

instruction_create_view = InstructionCreateView.as_view()

class InstructionReadView(View):

    def get(self, request, instruction_id):
        """Get specific instruction

        Args:
            request (HttpRequest): The request
            instruction_id (int): The id of the instruction
        """
        print("InstructionReadView.get")
        possible = "possible" in request.GET
        edit = "edit" in request.GET

        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_type = instruction.type
        action = instruction_type.action
        agent = action.agent
        if not possible:
            elements = list(InstructionElementAgentCall.objects.filter(instruction_type=instruction_type)) \
                    + list(InstructionElementMessage.objects.filter(instruction_type=instruction_type)) \
                    + list(InstructionElementTextInput.objects.filter(instruction_type=instruction_type)) \
                    + list(InstructionElementDocumentLink.objects.filter(instruction_type=instruction_type)) \
                    + list(InstructionElementRevise.objects.filter(instruction_type=instruction_type))
            elements.sort(key=lambda x: x.index)
        else:
            elements = []
        
        element_types = InstructionElementType.objects.all()
        
        context = {
            "action": action
            ,"instruction": instruction
            ,"agent": agent
            ,"elements": elements
            ,'element_types': element_types
            ,"possible": possible
            ,"edit": edit
        }
        return render(request, "components/instructionComponent/instruction.html", context)
    
    @staticmethod
    def forward(response, instruction):
        print("InstructionReadView.forward")
        url = reverse("instruction:read", kwargs={"instruction_id":instruction.pk})
        html = f"<div hx-trigger='load' hx-get='{url}' hx-target='#instruction-{instruction.pk}'></div>"
        response.write(html)
        print(html)
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
        if instruction.template:
            print("Error: Template instructions shouldn't be deleted")
            return HttpResponse('')
        task = instruction.task
        instruction.delete()
        if task:
            response = HttpResponse()
            response = InstructionIndexView.forward(response, get={"task":task.pk, "action":instruction.type.action.pk}) # Refresh all instructions
            return response
        else:
            return HttpResponse('')
    
    @staticmethod
    def forward(response, instruction):
        url = reverse("instruction:read", kwargs={"instruction_id":instruction.pk})
        response.write(f"<div hx-trigger='load' hx-get='{url}' hx-target='#instruction-{instruction.pk}' hidden></div>")
        return response
    
instruction_delete_view = InstructionDeleteView.as_view()

class InstructionCreateFromTemplateView(View):
    """
    Create a new instruction from a template instruction.

    This is done when the user clicks on the "Create" button in the possible instructions, project view.
    """

    def post(self, request, instruction_id):
        print("InstructionCreateFromTemplateView.post")
        task = get_object_or_404(Project, id=request.POST["task_id"])
        instruction = get_object_or_404(Instruction, id=instruction_id)

        instruction.pk = None
        instruction._state.adding = True
        instruction.template = False
        instruction.task = task
        instruction.save()

        return render(request, "components/instructionComponents/instruction.html", {"instruction": instruction})

instruction_create_from_template_view = InstructionCreateFromTemplateView.as_view()

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