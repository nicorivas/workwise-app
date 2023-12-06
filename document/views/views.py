import logging
import json

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q

from document.models import Document, DocumentSource
from instruction.models import Instruction, Message
from task.models import Task
from projects.models import Project

class DocumentIndexView(View):
    
    def get(self, request):
        print("DocumentIndexView.get")
        documents = Document.objects.all()
        document_sources = DocumentSource.objects.all()
        context = {
            "documents": documents,
            "document_sources": document_sources,
        }
        return render(request, "document/index.html", context)

    def post(self, request):
        print("DocumentIndexView.post")
        documents = Document.objects.all()
        document_sources = DocumentSource.objects.all()
        context = {
            "documents": documents,
            "document_sources": document_sources,
        }
        return render(request, "document/main.html", context)

document_index_view = DocumentIndexView.as_view()

class DocumentIndexJsonView(View):
    
    def get(self, request):
        print("DocumentIndexJsonView.get")
        documents = list(Document.objects.values('pk','name','type','author_agent__type__name'))
        print(documents)
        data = {"data":documents}
        return JsonResponse(data, safe=False)

document_index_json_view = DocumentIndexJsonView.as_view()

class DocumentCreateView(View):
    
    def post(self, request):
        # Create a new document
        print("DocumentCreateView.post", request.POST)

        # If it was created in the context of a task, get the task
        try:
            task_id = request.POST.get('task_id')
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            task = None

        # If it was created in the context of a task, get the task
        try: 
            project_id = request.POST.get('project_id')
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            project = None

        # If it was created in the context of a task, get the task
        try:
            parent_document_id = request.POST.get('parent_document_id')
            parent_document = Document.objects.get(pk=parent_document_id)
        except Document.DoesNotExist:
            parent_document = None

        name = request.POST.get('name', "New Document")
        type = request.POST.get('type', "General")

        document = Document(
            name=name,
            type="General",
            parent_document=parent_document,
            is_format=json.loads(request.POST.get('is_format', False)), # JSON used to convert string to boolean
            task=task,
            project=project,
            )
        document.save()

        # If it was created in the context of a task, set the current document of the task to the one created
        if task_id:
            task.active_document = document
            task.save()

        return JsonResponse({"document_id":document.pk}, safe=False)

        if not task_id:
            context = {
                "document": document,
            }
            return render(request, "document/document.html", context)
        else:
            context = {
                "task": task,
            }
            return render(request, "task/documents.html", context)

class DocumentReadView(View):
    
    def get(self, request, document_id):
        print("DocumentReadView.get", request.GET)

        document = get_object_or_404(Document, pk=document_id)
        if document.task:
            document.task.active_document = document
            document.task.save()

        if document.is_format:
            query = (Q(parent_document=document.parent_document) & Q(is_format=True))
            formats = Document.objects.filter(query)
        else:
            query = (Q(parent_document=document) & Q(is_format=True))
            formats = Document.objects.filter(query)

        print("DocumentReadView.get:formats", formats)

        context = {
            "document": document,
            "formats": formats,
            "hola":"caca"
        }
        return render(request, "document/document.html", context)

class DocumentUpdateView(View):
    
    def post(self, request, document_id):
        print("DocumentUpdateView.post", request.POST)
        document = get_object_or_404(Document, pk=document_id)
        document.clear_elements()
        document.create_elements_from_reply(request.POST.get('text'), markdown=request.POST.get('markdown'))
        document.save()
        context = {
            "document": document,
        }
        return render(request, "document/document.html", context)
    
class DocumentDeleteView(View):
    
    def post(self, request, document_id):
        print("DocumentDeleteView.post", request.POST)
        document = get_object_or_404(Document, pk=document_id)
        document.delete()
        return JsonResponse({"status": "success"})
    
class DocumentHeaderView(View):

    context = {}
    
    def get(self, request, document_id):
        print("DocumentHeaderView.get")
        self.get_document(document_id)
        return render(request, "document/header.html", self.context)
    
    def post(self, request, document_id):
        print("DocumentHeaderView.post",request.POST)
        self.get_document(document_id)
        
        # Forward
        forward_url_name = request.POST.get('forward_url_name')
        if forward_url_name:
            forward_url = reverse(request.POST.get('forward_url_name'),args=[document_id])
            forward_target = request.POST.get('forward_target')
            if forward_target:
                self.context["forward"] = {'url':forward_url, 'target':forward_target}
            else:
                logging.warning("No forward target given")
        else:
            logging.warning("No forward url given")

        return render(request, "document/header.html", self.context)
    
    def get_document(self, document_id):
        document = get_object_or_404(Document, pk=document_id)
        self.context = {
            "document": document,
        }
    
class DocumentBodyView(View):
    
    def get(self, request, document_id):
        print("DocumentBodyView.get")
        document = get_object_or_404(Document, pk=document_id)
        context = {
            "document": document,
        }
        return render(request, "document/body.html", context)
    
class DocumentRefreshView(View):
    
    @staticmethod
    def forward(response, document):
        print("DocumentRefreshView.forward")
        url = reverse("document:refresh", kwargs={"document_id":document.pk})
        html = f"<div hx-trigger='load' hx-get='{url}' hx-target='#document__body-{document.pk}'></div>"
        response.write(html)
        return response
    
class DocumentReviseView(View):

    def get(self, request, document_id):
        print("DocumentReviseView.get")
        document = get_object_or_404(Document, pk=document_id)
        instruction_revise = Instruction.objects.get(type__name="Revise Project Charter", project__document=document)
        instruction_revise.delete_messages()
        for element in document.get_elements():
            instruction_revise.add_message(text="", message_kwargs={"title":element.title, "mimesis_action":"./mimesis/library/project_charter/ReviseProjectCharterSection"})

        return redirect("instruction:read", instruction_id=instruction_revise.pk)
    
    @staticmethod
    def forward(response, document):
        """
        Forward to the revision of the document. This is called after a document is read.
        """
        print("DocumentReviseView.forward")
        url = reverse("document:revise", kwargs={"document_id":document.pk})
        instruction_revise = Instruction.objects.get(type__name="Revise Project Charter", project__document=document)
        html = f"<div hx-trigger='load' hx-get='{url}' hx-target='#instruction-{instruction_revise.pk}'></div>"
        response.write(html)
        return response

class DocumentClearView(View):
    
    def post(self, request, document_id):
        print("DocumentClearView.get")
        document = get_object_or_404(Document, pk=document_id)
        document.clear_elements()
        document.save()
        return redirect("document:read", document_id=document.pk)

class DocumentViewView(View):

    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        context = {
            "document": document,
        }
        return render(request, "document/view.html", context)
    
# API

class DocumentReadApiView(View):
    
    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        if document.json:
            if isinstance(document.json, dict):
                return JsonResponse(document.json, safe=True)
            else:
                return JsonResponse(json.loads(document.json), safe=True)
        else:
            blocks = [{
                "type": "paragraph",
                "data": {"text": ""}}]
            return JsonResponse({"time": 1698280894778, "blocks": blocks, "version": '2.28.2'})
        
class DocumentReadReplyApiView(View):
    
    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        return JsonResponse({"reply": document.reply})
    
class DocumentSaveApiView(View):
        
    def post(self, request, document_id):
        print("DocumentSaveApiView.post", document_id)
        document = get_object_or_404(Document, pk=document_id)
        document.clear_elements()
        document.reply = request.POST.get('document_reply')
        document.json = request.POST.get('document_json')
        document.save()
        return JsonResponse("{}", safe=False)
    
class DocumentFormatView(View):

    def post(self, request, document_id):
        print("DocumentFormatView.post", request.POST)
                
        # Get current task from request
        task_id = request.POST.get('task')
        if task_id:
            task = get_object_or_404(Task, pk=task_id)
        
        # Create document of new format
        document = get_object_or_404(Document, pk=document_id)
        # The active document might be a format, so we change to the parent document
        if document.parent_document != None and document.is_format == True:
            print(document)
            document = document.parent_document
            print(document)

        # Check if we already have a document of this format
        document_format = Document.objects.filter(parent_document=document, is_format=True) # THIS IS WRONG, WE NEED TO FILTER BY FORMAT
        if not document_format:
            # If we still don't have this document, create it
            document_format = document.create_format(format)
            document_format.save()
        else:
            document_format = document_format[0]
            document_format.update_format(document, format)
        
        # If task is present set document as new active one.
        if task_id:
            task.active_document = document_format
            task.save()
        
        if task_id:
            # If we are in the context of a task, render again all documents.
            context = {
                "task": task,
            }
            return render(request, "task/documents.html", context)
        else:
            return redirect("document:read", document_id=document_format.pk)

document_format_view = DocumentFormatView.as_view()

#

class DocumentSectionsSaveView(View): 

    def post(self, request, document_id):
        print("DocumentSectionsSaveView.post", request.POST)
        document = get_object_or_404(Document, pk=document_id)
        document.sections = json.loads(request.POST.get('sections'))
        document.save()
        return JsonResponse({"status": "success"})