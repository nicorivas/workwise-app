from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse, HttpResponse
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from django.shortcuts import redirect

import json
import time
import openai

from .models import Project, Record
from document.models import Document
from actions.models import Action
from company.models import Company
from task.models import Task
from instruction.models.instruction import Instruction
from task.forms import TaskCreateForm
from projects.forms import ProjectCreateForm


def index_context(request, context=None):
    """Get context for index view.
    We use this function as this is also called by project read, as index and read share the template.
    """
    projects = Project.objects.order_by("index", "name").values("pk", "name", "index")
    if request.user.is_authenticated:
        projects = projects.filter(company=request.session.get("company_id"))

    records = Record.objects.defer()

    if not context:
        context = {}
        context["project_create_form"] = ProjectCreateForm()

    context["projects"] = projects
    context["records"] = records

    return context


def transcribe_audio(request, project_id):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return JsonResponse({"text":transcript["text"]}, safe=False)

    return JsonResponse({'error': 'Invalid method'})

def record(request):
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")
        language = request.POST.get("language")
        Record.objects.create(language=language, voice_record=audio_file)
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse({ "success": True })
    
    context = {"page_title": "Record audio"}
    return render(request, "core/record.html", context)

def record_detail(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    context = {
        "page_title": "Recorded audio detail",
        "record": record,
    }
    return render(request, "core/record_detail.html", context)

class ProjectIndexView(View):

    def get(self, request):
        """Index view of projects, shows list.
        """
        print("ProjectIndexView.get", request.GET)

        context = index_context(request)

        if request.GET.get("source") == "menu":
            return render(request, "projects/index_main.html", context)
        else:
            return render(request, "projects/index.html", context)

project_index_view = ProjectIndexView.as_view()

class ProjectCreateView(View):

    def post(self, request):
        """Create new project

        Args:
            request (HttpRequest): Django request object
                company_id (int): Company ID
                action (int): Action ID

        """
        print("ProjectCreateView.post", request.POST)

        # Create project
        # Get company, from session data.
        company = get_object_or_404(Company, pk=request.session.get("company_id"))
        project = Project.objects.create(
            name=request.POST.get("name","New project"),
            description=request.POST.get("description"),
            company=company,
            created_by=request.user)
        project.save()

        # Sometimes we get an action, if project was created by clicking on explorer action
        action_id = request.POST.get("action")
        if action_id:
            action = get_object_or_404(Action, pk=int(action_id))

            # Add first task to project, and create all instructions for it
            task = Task(name=action.name, project=project, action=action, created_by=request.user)
            task.save()
            Instruction.create_from_task(task)

            # Add first blank document to task
            document = Document(name=f"New document: {action.name}", task=task, author_user=request.user)
            document.save()

            # Set active document on task to newly created document
            task.active_document = document
            task.save()

            return redirect("task:read_index", task_id=task.pk)
        else:
            return render(request, "projects/menu_item.html", {"project":project})

project_create_view = ProjectCreateView.as_view()

class ProjectReadView(View):
    
    def get(self, request, project_id: int):
        """Read project, that is, show the main view of a project

        Args:
            request (HttpRequest): Django request object
            project_id (int): Project ID
        """
        print("ProjectReadView.get", request.GET)
        project = get_object_or_404(Project, pk=project_id)
                
        context = {
            "project": project
            ,"task_create_form": TaskCreateForm()
        }

        if request.GET.get("source") == "menu":
            print("return details")
            return render(request, "projects/details.html", context)
        else:
            context = index_context(request, context)
            return render(request, "projects/index.html", context)

project_read_view = ProjectReadView.as_view()

def update_name(request, project_id:int):
    project = get_object_or_404(Project, pk=project_id)
    project.name = request.POST.get("name")
    project.save()
    return JsonResponse({"name": project.name})

class ProjectDeleteView(View):

    def post(self, request, project_id:int):
        """Delete project
        """
        print("ProjectDeleteView.post", request.POST)

        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return HttpResponse()
    
project_delete_view = ProjectDeleteView.as_view()

@csrf_exempt
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    instruction_id = message.instruction.pk
    message.delete()
    messages = Message.objects.filter(instruction=instruction_id)
    context = {
        "messages": messages
    }
    return render(request, "projects/messages.html", context)


class ProjectContextView(View):

    def get(self, request, project_id:int):
        """Project context
        """
        print("ProjectContextView.get", request.GET)

        project = get_object_or_404(Project, pk=project_id)
        context = {
            "project": project
        }
        return render(request, "projects/table_context.html", context)
    
project_context_view = ProjectContextView.as_view()