import openai

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from document.models import Document
from instruction.models import Instruction
from task.forms import TaskCreateForm
from task.models import Task
from mimesis.agent.agent import Agent as MimesisAgent
from datetime import datetime

class TaskIndexView(View):
    
    def get(self, request, *args, **kwargs):
        # Render index page with all tasks
        
        # Get parameters from url
        project_id = request.GET.get("project_id", None)

        # Get all parameters
        tasks = Task.objects.all()

        # Filter by given parameters, if they exist
        if project_id:
            tasks = Task.objects.filter(project__pk=project_id)

        # Create a new form instance
        form = TaskCreateForm()

        # Build context
        context = {
            "tasks": tasks
            ,"form": form
        }

        return render(request, "task/index.html", context)

task_index_view = TaskIndexView.as_view()

class TaskCreateView(View):
    
    def post(self, request, *args, **kwargs):
        print("TaskCreateView.post", request.POST)
        # Create a new task based on contents of form

        # Create a new form instance, populate it with data from the request
        form = TaskCreateForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            task = form.save(commit=False)
            task.created_by = request.user
            task.created_at = datetime.now()
            task.updated_at = datetime.now()
            task.save()

            if request.POST.get("source") == "explorer":

                # Add first blank document to task
                document = Document(name=f"New document: {task.name}", task=task, author_user=request.user)
                document.save()

                # Set active document on task to newly created document
                task.active_document = document
                task.save()

                # Create instructions of task
                Instruction.create_from_task(task)

                return redirect("task:read_index", task_id=task.pk)
            
            else:

                # Add first blank document to task
                document = Document(name=f"New document: {task.name}", task=task, author_user=request.user)
                document.save()

                # Set active document on task to newly created document
                task.active_document = document
                task.save()

                # Create instructions of task
                Instruction.create_from_task(task)

                # Re-render index
                tasks = Task.objects.filter(project__pk=request.POST.get("project", None))
                form = TaskCreateForm()
                context = {
                    "tasks": tasks
                    ,"form": form
                }
                
                return render(request, "projects/details_tasks.html", context)
        else:
            # Form is not valid
            print(form.errors.values())
            pass


task_create_view = TaskCreateView.as_view()

class TaskReadIndexView(View):
    
    def get(self, request, *args, **kwargs):

        # Create mimesis Agent to store in session
        mms_agent = MimesisAgent(name="Agent", definition="Doesn't matter")
        request.session['agent'] = mms_agent.json()

        # Render a particular task.
        task = Task.objects.get(pk=kwargs["task_id"])
        # Get instructions that reference this task
        instructions = task.instruction_set.all()
        # Build context
        context = {
            "task": task
            ,"instructions": instructions
        }
        return render(request, "task/task_index.html", context)

task_read_index_view = TaskReadIndexView.as_view()

class TaskReadView(View):
    
    def get(self, request, *args, **kwargs):
        # Render a particular task.
        task = Task.objects.get(pk=kwargs["task_id"])
        # Get instructions that reference this task
        instructions = task.instruction_set.all()
        # Build context
        context = {
            "task": task
            ,"instructions": instructions
        }
        return render(request, "task/task.html", context)

task_read_view = TaskReadView.as_view()

class TaskReadDocumentsView(View):
    
    def get(self, request, *args, **kwargs):
        # Render the documents of a particular task.
        task = Task.objects.get(pk=kwargs["task_id"])
        # Build context
        context = {
            "task": task
        }
        return render(request, "task/documents.html", context)

task_read_documents_view = TaskReadDocumentsView.as_view()

class TaskDeleteView(View):
    
    def post(self, request, *args, **kwargs):
        print("TaskDeleteView.post", request.POST)

        task = Task.objects.get(pk=request.POST.get("task_id", None))
        task.delete()
        return JsonResponse({"status": "success"})

task_delete_view = TaskDeleteView.as_view()

def transcribe_audio(request, project_id):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return JsonResponse({"text":transcript["text"]}, safe=False)

    return JsonResponse({'error': 'Invalid method'})