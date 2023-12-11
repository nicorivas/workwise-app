import openai
import json
import logging
import markdown

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from instruction.models import Feedback
from projects.models import Project
from company.models import Company
from actions.models import Action
from task.models import Task
from instruction.models import Instruction
from document.models import Document
from user.views import user_create_view
from company.views import company_create_view
from .models import Pitch, Flow
from .forms import PitchCreateForm, FlowRegisterForm

class FlorIndexView(View):
    
    def get(self, request):

        return render(request, "flow/index.html")

flow_index = FlorIndexView.as_view()

class FlowReadView(View):

    def get(self, request, flow_id=None, task_id=None):

        context = {}

        # Get flow
        flow = Flow.objects.get(pk=flow_id)
        context["flow"] = flow

        # Get task, if given
        if task_id:
            task = Task.objects.get(pk=task_id)
            context["task"] = task
            context["document"] = task.active_document

        # Fill registration form
        form = FlowRegisterForm()
        if task_id:
            form.fields["author_name"].initial = task.created_by.profile.full_name
            form.fields["author_email"].initial = task.created_by.email
        context["form"] = form

        if task_id:
            instructions = Instruction.objects.filter(task=task, type__flow_visible=True).select_related("type")
            context["instructions"] = instructions

        return render(request, "flow/flow.html", context)

flow_read = FlowReadView.as_view()

class FlowCarozziIndexView(View):
    
    def get(self, request, pitch_id=None):

        form = None
        pitch = None

        if pitch_id:
            pitch = Pitch.objects.get(pk=pitch_id)
            form = PitchCreateForm(instance=pitch)
            context = {"form": form, "pitch": pitch}
        else:
            form = PitchCreateForm()

        context = {"form": form, "pitch": pitch}

        return render(request, "flow/index.html", context)

flow_carozzi_index = FlowCarozziIndexView.as_view()

class FlowCreateTask(View):
    
    def post(self, request):

        logging.warning("FlowCreateTask:post" + str(request.POST))

        # Validate form
        form = FlowRegisterForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"status": "error", "errors": form.errors}, safe=False)

        # Create or get company
        company_data = company_create_view(request).content
        company_data = json.loads(company_data.decode('utf-8'))
        company = Company.objects.get(pk=company_data["id"])

        # Create or get user
        user_data = user_create_view(request).content
        user_data = json.loads(user_data.decode('utf-8'))
        user = User.objects.get(pk=user_data["id"])
        user.profile.companies.add(company)
        user.profile.full_name = request.POST["author_name"]
        user.profile.save()

        logging.warning("FlowCreateTask:post" + str(user))
        logging.warning("FlowCreateTask:post" + str(user.profile.full_name))

        project = Project.objects.get(pk=request.POST["project"])
        action = Action.objects.get(pk=request.POST["action"])
        
        # Create task
        task = Task.objects.create(
            name="Task Flow"
            ,project=project
            ,action=action
            ,created_by=user)

        # Create document
        document = Document(name=f"New document: {task.name}", task=task, author_user=user)
        document.save()

        task.active_document = document
        task.save()

        Instruction.create_from_task(task)
        instructions = Instruction.objects.filter(task=task, type__flow_visible=True)

        return render(request, "flow/task.html", {"task": task, "instructions": instructions})

flow_create_task = FlowCreateTask.as_view()

class FlowSendEmail(View): 
    
    def post(self, request, flow_id, task_id):

        from django.core.mail import EmailMultiAlternatives

        logging.warning("FlowSendEmail:post" + str(request.POST))

        flow = Flow.objects.get(pk=flow_id)
        task = Task.objects.get(pk=task_id)
        instructions = Instruction.objects.filter(task=task, type__flow_visible=True)
        pitch = instructions[0].data["power_pitch"]
        analysis = task.active_document.reply
        analysis_html = markdown.markdown(analysis)
        html_message = render_to_string('flow/mail.html', {'task': task, 'pitch': pitch, 'analysis': analysis_html})
        plain_message = strip_tags(html_message)

        msg = EmailMultiAlternatives(
            f'Análisis de pitch',
            plain_message,
            'nico@getworkwise.ai',
            [task.created_by.email],
            ["christian.ortiz@brinca.com "],
            reply_to=["nico@getworkwise.ai"],
            headers={"Message-ID": "foo"},
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        
        return JsonResponse({"status": "ok"}, safe=False)
        
flow_send_email = FlowSendEmail.as_view()