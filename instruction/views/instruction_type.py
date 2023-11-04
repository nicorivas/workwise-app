import urllib

from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse

from ..models import Instruction, InstructionType, InstructionElementAgentCall, InstructionElementMessage, InstructionElementTextInput, InstructionElementDocumentLink, InstructionElementRevise
from ..forms import InstructionTypeCreateForm, InstructionTypeUpdateForm, InstructionElementCreateForm
from ..views import InstructionIndexView

class InstructionTypeCreateView(View):
    """Create a new InstructionType. This view is called from the action page, and it returns the id of the new InstructionType.

    This also creates a template instruction, to be used in the action page.
    
    Returns:
        JsonResponse: The id of the new InstructionType.
    """
    def post(self, request):
        print("InstructionTypeCreateView.post", request.POST)
        response = HttpResponse()
        form = InstructionTypeCreateForm(request.POST)
        if form.is_valid():
            instruction_type = form.save()
            # We create a template instruction to use in the action page
            instruction = Instruction(type=instruction_type, template=True)
            instruction.save()
            url = reverse("instruction:index")
            querystring = urllib.parse.urlencode({"action":instruction_type.action.pk,"template":"1","edit":"1"})
            return HttpResponseRedirect(f"{url}?{querystring}")
        
        return JsonResponse({"error": "Form is not valid"})

instruction_type_create_view = InstructionTypeCreateView.as_view()

class InstructionTypeReadView(View):
    def get(self, request, instruction_type_id):
        instruction_type = get_object_or_404(InstructionType, id=instruction_type_id)
        action = instruction_type.action
        agent = action.agent
        instruction_element_create_form = InstructionElementCreateForm()
        instruction_elements = list(InstructionElementAgentCall.objects.filter(instruction_type=instruction_type)) \
            + list(InstructionElementMessage.objects.filter(instruction_type=instruction_type)) \
            + list(InstructionElementTextInput.objects.filter(instruction_type=instruction_type)) \
            + list(InstructionElementDocumentLink.objects.filter(instruction_type=instruction_type)) \
            + list(InstructionElementRevise.objects.filter(instruction_type=instruction_type))
        instruction_elements.sort(key=lambda x: x.index)
        context = {
            "action": action
            ,"instruction_type": instruction_type
            ,"agent": agent
            ,"instruction_element_create_form": instruction_element_create_form
            ,"instruction_elements": instruction_elements
        }
        return render(request, "instruction/instruction_type.html", context)

instruction_type_read_view = InstructionTypeReadView.as_view()

class InstructionTypeUpdateView(View):
    def post(self, request, instruction_type_id):
        print("InstructionTypeUpdateView.post")
        print(request.POST)
        instruction_type = get_object_or_404(InstructionType, id=instruction_type_id)
        form = InstructionTypeUpdateForm(request.POST, instance=instruction_type)
        form.save()
        context = {
            "instruction_type": instruction_type
        }
        return render(request, "instruction/instruction_type.html", context)

instruction_type_update_view = InstructionTypeUpdateView.as_view()

class InstructionTypeDeleteView(View):
    def get(self, request, instruction_type_id):
        instruction_type = get_object_or_404(InstructionType, id=instruction_type_id)
        instruction_type.delete()
        return HttpResponse('')
    
instruction_type_delete_view = InstructionTypeDeleteView.as_view()