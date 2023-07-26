from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
import json

import openai

from .models import Project, Record, Message, Instruction, Document
from actions.models import ActionDB

from mimesis.agent.agent import Agent
from mimesis.actions.project import EvaluatePrompt, WriteProject

openai.api_key = settings.OPENAI_API_KEY

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
def call_action(request, project_id, instruction_id, action_id):
    if request.method == 'POST':
        print("call_action", project_id, action_id, instruction_id)
        instruction = get_object_or_404(Instruction, id=instruction_id)
        agent = Agent(**json.loads(request.session['agent']))
        action = EvaluatePrompt(project_description=request.POST.get("prompt"))
        reply = agent.do(action)
        project = get_object_or_404(Project, pk=project_id)
        agent = get_object_or_404(Project, pk=project_id)
        message = Message.objects.create(
            project=project,
            message=reply,
            agent=project.agent,
            instruction=instruction,
            user="Agent",
            type="comment"
            )
        message.save()
        context = {
            "instruction": instruction,
        }
        return render(request, "projects/instruction.html", context)

def parse_markdown(reply):
    reply = json.loads(reply)
    text = f"""# {reply["title"]}
"""

    text += """## Main objectives
"""
    for objective in reply["main_objectives"]:
        text += f"""- {objective["description"]}
"""

    text += f"""## Background
{reply["background"]}
"""

    text += f"""## Timeline
{reply["timeline"]}
"""
    text += """## Stakeholders
"""
    for stakeholder in reply["stakeholders"]:
        text += f"""- *{stakeholder["name"]}*: {stakeholder["role"]}
"""

    text += f"""## Risks & Assumptions
"""
    for rna in reply["risks_and_assumptions"]:
        text += f"""- *{rna["type"]}*: {rna["description"]}
"""

    return text

@csrf_exempt
def write_document(request, project_id, document_id):
    
    # Get document
    document = get_object_or_404(Document, id=document_id)

    # Generate agent
    agent = Agent(**json.loads(request.session['agent']))
    # Create and execute selected action
    action = WriteProject(project_description=request.POST.get("prompt"))
    reply = agent.do(action)

    # Parse reply to markdown
    markdown = parse_markdown(reply)

    # Update document with new body
    document.text = markdown
    document.save()

    # Return updated document
    context = {
        "document": document,
    }
    return render(request, "projects/document.html", context)

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
def get_prompt(request, project_id):
    if request.method == 'POST':
        agent = Agent(**json.loads(request.session['agent']))
        action = WriteProject(project_description=request.POST.get("prompt"))
        prompt = agent.prompt(action=action)
        context = {"prompt":prompt}
        return render(request, "projects/modal_prompt.html", context)

@csrf_exempt
def gatekeeper(request, project_id):
    if request.method == 'POST':
        message = request.POST.get("fields[message]")
        model: str = "gpt-3.5-turbo"
        llm_system = "You are a senior project manager with over 20 years of experience. You answer questions using markdown."
        llm_prompt = f"""
        Please consider the following transcript as context describing a new project: 
        {message}

        
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
    }
    return render(request, "projects/index.html", context)

def project(request, project_id):


    project = get_object_or_404(Project, pk=project_id)
    document = project.document
    agent = project.agent
    instructions = Instruction.objects.filter(project=project_id)

    # Create mimesis Agent to store in session
    mms_agent = Agent(name=agent.name, definition=agent.definition)
    request.session['agent'] = mms_agent.json()
    
    messages = Message.objects.filter(project=project_id, type="audio")
    context = {
        "project": project,
        "document": document,
        "instructions": instructions,
    }
    return render(request, "projects/project.html", context)

@csrf_exempt
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    instruction_id = message.instruction.pk
    print(instruction_id)
    message.delete()
    messages = Message.objects.filter(instruction=instruction_id)
    context = {
        "messages": messages
    }
    return render(request, "projects/messages.html", context)