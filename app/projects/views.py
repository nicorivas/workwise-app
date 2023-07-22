from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

import openai

from .models import Project, Record, Message
from actions.models import ActionDB

from mimesis.agent.agent import Agent

# This for Audio Recording

openai.api_key = "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"

@csrf_exempt
def actions(request, project_id):
    actions = ActionDB.objects.all()
    context = {
        "actions": actions,
    }
    return render(request, "projects/actions.html", context)

@csrf_exempt
def select_action(request, project_id, action_id):
    action = get_object_or_404(ActionDB, id=action_id)
    context = {
        "action": action,
    }
    return render(request, "projects/action.html", context)

@csrf_exempt
def call_action(request, project_id):
    if request.method == 'POST':
        print(request.POST)

        agent = Agent()

        messages = Message.objects.filter(project=project_id)
        context = {
            "messages": messages,
        }
        return render(request, "projects/messages.html", context)

@csrf_exempt
def transcribe_audio(request, project_id):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message = Message.objects.create(
            project_id=project_id,
            message=transcript["text"],
            user="Nico",
            type="audio"
            )
        message.save()
        serialized_obj = serializers.serialize('json', [message, ])
        return JsonResponse(json.loads(serialized_obj)[0], safe=False)

    return JsonResponse({'error': 'Invalid method'})

@csrf_exempt
def gatekeeper(request, project_id):
    print(request)
    if request.method == 'POST':
        print(request.POST)
        message = request.POST.get("fields[message]")
        model: str = "gpt-3.5-turbo"
        llm_system = "You are a senior project manager with over 20 years of experience. You answer questions using markdown."
        llm_prompt = f"""
        Please consider the following transcript as context describing a new project: 
        {message}

        From the project context, identify the following elements:
        * Project title.
        * The main objectives, ranging from 1 to a maximum of 3. Please use the SMART framework to write the objetives: each should be specific, measurable, achievable, relevant and time bound.
        * Identify the project background. This should summarize briefly why the project is necessary and how it will benefit the organization or users.
        * The project timeline, this should include the expected beginning and end dates. If those dates are not found in the context, please identify an estimated lenght in weeks or months. If you consider that you didn't found the project timeline in the context, assume it was "not found".
        * Project stakeholders, describing briefly how each is one is affected or should be involved in the project. If you consider that you didn't found enough information in the context to identify project stakeholders, assume it was "not found".
        * Risks and assumptions of the project. Describe each briefly, list a maximum of 5 risks and assumptions. If you consider that you didn't found enough information in the context to identify project stakeholders, assume it was "not found".

        Now, consider all the items you have analized and write down in markdown using the following order of headers: project title, main objectives, project background, project timeline, project stakeholders, and project risks and assumptions.
        """

        llm_messages = [{"role": "system", "content": llm_system}]
        llm_messages += [{"role": "user", "content": llm_prompt}]
        message = Message.objects.create(
            project_id=project_id,
            message=llm_prompt,
            user="System",
            type="llm_prompt"
            )
        message.save()
        response = openai.ChatCompletion.create(
            model=model,
            messages=llm_messages
            )
        reply = response["choices"][0]["message"]["content"]
        message = Message.objects.create(
            project_id=project_id,
            message=reply,
            user="Agent",
            type="llm_reply"
            )
        message.save()
        return JsonResponse({'message': "reply"})

def record(request):
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")
        language = request.POST.get("language")
        record = Record.objects.create(language=language, voice_record=audio_file)
        record.save()
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse(
            {
                "success": True,
            }
        )
    context = {"page_title": "Record audio"}
    return render(request, "core/record.html", context)


def record_detail(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    context = {
        "page_title": "Recorded audio detail",
        "record": record,
    }
    return render(request, "core/record_detail.html", context)

# Create your views here.

def index(request):
    projects = Project.objects.order_by("name")
    records = Record.objects.all()
    context = {
        "projects": projects,
        "records": records,
        "messages": messages,
    }
    return render(request, "projects/index.html", context)

def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    messages = Message.objects.filter(project=project_id, type="audio")
    context = {
        "project": project,
        "messages": messages,
    }
    return render(request, "projects/project.html", context)