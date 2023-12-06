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

        print("context", context)

        # Fill registration form
        form = FlowRegisterForm()
        if task_id:
            form.fields["author_name"].initial = task.created_by.profile.full_name
            form.fields["author_email"].initial = task.created_by.email
        context["form"] = form

        if task_id:
            instructions = Instruction.objects.filter(task=task, type__flow_visible=True)
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

        print("FlowCreateTask", request.POST)

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
        user.save()

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

class FlowTranscribe(View):
    
    def post(self, request):

        audio_file = request.FILES['audio']
        transcript = instruction_element.transcribe(audio_file)
        instruction = Instruction.objects.get(pk=request.POST.get("instruction"))
        instruction.data = {"pitch": transcript["text"]}
        instruction.save()

        response = {
            "text":transcript["text"]
        }

        audio_file.close()

        return JsonResponse(response, safe=False)
    
flow_transcribe = FlowTranscribe.as_view()

class FlowAnalyse(View):

    def post(self, request):

        print("FlowAnalyse:post", request.POST)

        pitch = Pitch.objects.get(pk=request.POST.get("pitch_id"))
        pitch.analyse(request)
        pitch.save()

        return JsonResponse({"status": "ok"}, safe=False)

flow_analyse = FlowAnalyse.as_view()

class FlowAnalyseLong(View):

    def post(self, request):
        
        from django.core.mail import send_mail
        
        pitch = Pitch.objects.get(pk=request.POST.get("pitch_id"))
        pitch.analyse_long(request)
        html = markdown.markdown(pitch.pitch_analysis_long)
        html_message = render_to_string('flow/mail.html', {'pitch': pitch, 'pitch_analysis_long_html': html})
        plain_message = strip_tags(html_message)
        send_mail(
            f'Análisis extendido de pitch sobre {pitch.startup_name}',
            plain_message,
            'nico@getworkwise.ai',
            [pitch.author_email],
            html_message=html_message,
            fail_silently=False)

        return JsonResponse({"status": "ok"}, safe=False)

flow_analyse_long = FlowAnalyseLong.as_view()


class FlowSendEmail(View): 
    
    def post(self, request):

        logging.warning("FlowSendEmail:post" + str(request.POST))

        from django.core.mail import send_mail
        send_mail('Subject here', 'Here is the message.', 'nico@getworkwise.ai', [
            'bernardita.ihnen@getworkwise.ai',
            'nicorivas@gmail.com'], fail_silently=False)
        
        return JsonResponse({"status": "ok"}, safe=False)
        
flow_send_email = FlowSendEmail.as_view()