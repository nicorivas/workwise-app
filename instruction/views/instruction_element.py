from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers

from ..forms import *
from instruction.models import *
# Forwards
from document.models import Document
from document.views import DocumentRefreshView, DocumentReviseView
from instruction.views.instruction import InstructionReadView

def get_element_and_form(element, instance=False, request=None):

    if element.type.name == element.type.InstructionElementTypes.MESSAGE:
        element = get_object_or_404(InstructionElementMessage, id=element.pk)
    elif element.type.name == element.type.InstructionElementTypes.TEXT_INPUT:
        element = get_object_or_404(InstructionElementTextInput, id=element.pk)    
    elif element.type.name == element.type.InstructionElementTypes.AGENT_CALL:
        element = get_object_or_404(InstructionElementAgentCall, id=element.pk)
    elif element.type.name == element.type.InstructionElementTypes.REVISE:
        element = get_object_or_404(InstructionElementRevise, id=element.pk)
    elif element.type.name == element.type.InstructionElementTypes.REVISION:
        element = get_object_or_404(InstructionElementRevision, id=element.pk)
    elif element.type.name == element.type.InstructionElementTypes.DOCUMENT_LINK:
        element = get_object_or_404(InstructionElementDocumentLink, id=element.pk)
    elif element.type.name == element.type.InstructionElementTypes.CHOICES:
        element = get_object_or_404(InstructionElementChoices, id=element.pk)

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
    elif element.type.name == element.type.InstructionElementTypes.REVISE:
        form = InstructionElementReviseUpdateForm(*form_args, **form_kwargs)
    elif element.type.name == element.type.InstructionElementTypes.DOCUMENT_LINK:
        form = InstructionElementDocumentLinkUpdateForm(*form_args, **form_kwargs)
    elif element.type.name == element.type.InstructionElementTypes.CHOICES:
        form = InstructionElementChoicesUpdateForm(*form_args, **form_kwargs)
    else:
        form = None
    
    return element, form

class InstructionElementIndexView(View):
    def get(self, request, instruction_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_elements = list(InstructionElementAgentCall.objects.filter(instruction_type=instruction.type)) \
            + list(InstructionElementMessage.objects.filter(instruction_type=instruction.type)) \
            + list(InstructionElementTextInput.objects.filter(instruction_type=instruction.type)) \
            + list(InstructionElementDocumentLink.objects.filter(instruction_type=instruction.type))
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
            print("form is valid")
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
            elif instruction_element.type.name == instruction_element.type.InstructionElementTypes.DOCUMENT_LINK:
                document_link = InstructionElementDocumentLink(name=instruction_element.name, instruction_type=instruction_type)
                document_link.save()
            
            return redirect("instruction:element_index", instruction_id=instruction.pk)

instruction_element_create_view = InstructionElementCreateView.as_view()

class InstructionElementReadView(View):

    def get(self, request, instruction_id:int, instruction_element_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element = get_object_or_404(InstructionElement, id=instruction_element_id)
        instruction_element, form = get_element_and_form(instruction_element, instance=False)

        context = {"instruction": instruction, "element": instruction_element, "form": form}

        if instruction_element.type.name == instruction_element.type.InstructionElementTypes.DOCUMENT_LINK:
            context["documents"] = Document.objects.all()

        return render(request, "instruction/elements/element.html", context)

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

class InstructionElementTranscribeView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element_text_input = get_object_or_404(InstructionElementTextInput, id=instruction_element_id)
        transcript = instruction_element_text_input.transcribe(request.FILES['audio'])
        instruction.data = {instruction_element_text_input.name: transcript["text"]}
        instruction.save()

        return JsonResponse({"transcript": transcript["text"]}, safe=False)

instruction_element_transcribe_view = InstructionElementTranscribeView.as_view()

class InstructionElementCallView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int, stream=True):
        """Triggered by call elements on push of button.

        We call the agent and update what is necessary after the agent call.
        Agent is called on model of the InstructionElementAgentCall.call_agent().

        Args:
            request (HttpRequest): Request object
            instruction_id (int): Instruction id
            action_element_id (int): Action element id
        """
        print("InstructionElementCallView.post")

        # Get objects
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction.delete_messages()
        instruction_element_agent_call = get_object_or_404(InstructionElementAgentCall, id=instruction_element_id)

        # Bulk of process, we call the agent through the model, InstructionElementAgentCall.call_agent()
        replies = instruction_element_agent_call.call_agent(request, instruction)
        
        # Compile a response based on type of reply.
        response = HttpResponse()
        document = None
        if instruction.task:
            for reply in replies:
                if reply["type"] == "format":
                    # If reply is format, then create a new format document
                    document = instruction.task.get_active_document()
                    document.create_format(instruction.type.name, reply["text"])
                if reply["type"] == "document":
                    # If reply is document, then clear and replace the document with the reply.
                    document = instruction.task.get_active_document()
                    document.clear_elements()
                    document.create_elements_from_reply(reply["text"], markdown=True)
                    document.save()
                if reply["type"] == "message":
                    # If reply is message, then clear all messages and add this new one.
                    instruction.add_message(reply["text"], message_kwargs={"title":"Test"}, set_text_kwargs={"split_on":[("#", "Section")]})
            
            # Forwards
            if reply["type"] == "document" or reply["type"] == "format":
                response = DocumentRefreshView.forward(response, document) # Refresh the document
                if reply["revise"]:
                    response = DocumentReviseView.forward(response, document) # Trigger revision of the document
            response = InstructionReadView.forward(response, instruction) # Refresh the instruction

        return response

instruction_element_call_view = InstructionElementCallView.as_view()

class InstructionElementCallPromptView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        """Triggered by call elements on push of button, when we want to get a prompt.
        """
        print("InstructionElementCallPromptView.post")
        instruction = get_object_or_404(Instruction, id=instruction_id)
        agent_call = get_object_or_404(InstructionElementAgentCall, id=instruction_element_id)
        prompt = agent_call.call_agent(request, instruction, stream=True)
        document = instruction.task.get_active_document()
        document.clear_elements()
        return JsonResponse({'prompt': prompt})
    
instruction_element_call_prompt_view = InstructionElementCallPromptView.as_view()

class InstructionElementReviseView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        """
        This is called when the button to get Feedback on a document is clicked.
        Feedback is called revision on the back.
        All things are done ont he corresponding revise model, InstructionElementRevise.
        """
        print("InstructionElementReviseView.post")

        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element_revise = get_object_or_404(InstructionElementRevise, id=instruction_element_id)

        # We call the agent through the model, InstructionElementRevise.call()
        # This call generates InstructionElementRevision elements that become part of the instruction.
        instruction_element_revise.call(request, instruction)

        # Return the instruction, as we've created new elements and we want to render them.
        return redirect("instruction:read", instruction_id=instruction.pk)

instruction_element_revise_view = InstructionElementReviseView.as_view()

class InstructionElementRevisionCallView(View):

    def post(self, request, instruction_id:int, instruction_element_id:int):
        print("InstructionElementRevisionCallView.post")

        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element_revision = get_object_or_404(InstructionElementRevision, id=instruction_element_id)
        instruction_element_revision.call_agent(request, instruction)

        return redirect("instruction:element_read", instruction_id=instruction.pk, instruction_element_id=instruction_element_revision.pk)

instruction_element_revision_call_view = InstructionElementRevisionCallView.as_view()

class InstructionElementDocumentLinkView(View):

    def get(self, request, instruction_id:int, instruction_element_id:int):
        print("InstructionElementDocumentLinkView.get")

        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction_element = get_object_or_404(InstructionElement, id=instruction_element_id)
        documents = Document.objects.all().order_by("-imported", "name")
        context = {"instruction": instruction, "element": instruction_element, "documents": documents}

        return render(request, "instruction/elements/document_link_documents.html", context)
    
    def post(self, request):
        print("InstructionElementDocumentLinkView.post")

        # Get document from request
        document_id = request.POST["document_id"]
        document = get_object_or_404(Document, id=document_id)

        # Get element from request
        instruction_element_id = request.POST["instruction_element_id"]
        instruction_element = get_object_or_404(InstructionElementDocumentLink, id=instruction_element_id)
        
        # Update element with document
        instruction_element.document = document
        instruction_element.save()

        return HttpResponse(document.name)


instruction_element_document_link_view = InstructionElementDocumentLinkView.as_view()

# API

class InstructionElementCreateAPI(View):
    # THIS SHOULD BE IMPLEMENTED BY DJANGO REST.

    def post(self, request):
        type = InstructionElementType.objects.get(name=request.POST.get("type", None))
        name = request.POST.get("name", None)
        index = request.POST.get("index", None)
        instruction = Instruction.objects.get(id=request.POST.get("instruction", None))
        mimesis_action = request.POST.get("mimesis_action", None)
        document = Document.objects.get(id=request.POST.get("document", None))
        document_section_index = request.POST.get("document_section_index")
        revision = InstructionElementRevision(
            type=type
            ,instruction_type=instruction.type
            ,name=name
            ,index=index
            ,mimesis_action=mimesis_action
            ,document=document
            ,document_section_index=document_section_index
            )
        revision.save()
        return JsonResponse(serializers.serialize("json", [revision]), safe=False)

instruction_element_create_api = InstructionElementCreateAPI.as_view()