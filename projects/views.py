from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.contrib import messages
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
from instruction.models.instruction import Instruction

from mimesis.agent.agent import Agent
from mimesis.actions.project import EvaluatePrompt, WriteProjectCharter, ReviseProjectCharter, ApplyRevisionCharter
from mimesis.actions.feedback import FeedbackGuidelines, FeedbackValues

from langchain.text_splitter import MarkdownHeaderTextSplitter

@csrf_exempt
def write_document(request, project_id, document_id, instruction_id):
    print("write_document")
    
    # Get project
    project = get_object_or_404(Project, id=project_id)
    document = get_object_or_404(Document, id=document_id)
    instruction = get_object_or_404(Instruction, id=instruction_id)

    # Remove follow-up instructions in case they existed
    Instruction.objects.filter(previous_instruction=instruction).delete()

    # Generate agent, and execute selected action
    agent = Agent(**json.loads(request.session['agent']))
    action = WriteProjectCharter(project_description=instruction.prompt)
    reply = agent.do(action)

    # Add reply to document. First clear all document.
    document.clear()
    document.text = reply
    document.create_element_from_reply(markdown=True)
    document.save()

    # Return updated document
    context = {
        "document": document,
    }
    context = forward(request,context, instruction_id)
    return render(request, "document/document.html", context)

@csrf_exempt
def revise_document(request, project_id, document_id, instruction_id):
    print("revise_document")
    
    # Get objects
    project = get_object_or_404(Project, id=project_id)
    document = get_object_or_404(Document, id=document_id)
    instruction = get_object_or_404(Instruction, id=instruction_id)
    
    # Generate agent
    agent = Agent(**json.loads(request.session['agent']))
    action = ReviseProjectCharter(project_charter=document.text)
    reply = agent.do(action)
    
    headers_to_split_on = [
        ("##", "Section"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(reply)
    print(md_header_splits)

    message = Message.objects.create(
        project=project,
        instruction=instruction,
        message=reply,
        user="Agent",
        type="project_charter_revision"
    )
    message.save()

    for section_obj in md_header_splits:
        content = section_obj.page_content
        section = section_obj.metadata.get("Section")
        if section:
            text = "## " + section + "\n" + content
        else:
            text = content
        block = MessageBlock.objects.create(message=message, text=text)
        block.generate_html()
        block.save()

    # Return updated document
    context = {
        "document": document,
    }
    context = forward(request,context,document_id)
    return render(request, "document/document.html", context)

def select_message_block(request, project_id, message_block_id):
    print("select_message_block")
    project = get_object_or_404(Project, id=project_id)
    message_block = get_object_or_404(MessageBlock, id=message_block_id)

    message_block.selected = not message_block.selected
    message_block.save()

    return render(request, "projects/message_block.html", {"project":project, "block": message_block})

@csrf_exempt
def apply_revision(request, project_id, document_id):
    print("apply_revision")

    # Get document
    document = get_object_or_404(Document, id=document_id)
    document.clear()

    agent = Agent(**json.loads(request.session['agent']))
    message = Message.objects.filter(project=project_id).filter(type="project_charter_revision").last()

    action = ApplyRevisionCharter(project_charter=document.text, project_revisions=message.text())
    reply = agent.do(action)

    document.text = reply
    document.create_element_from_reply(markdown=True)
    document.save()

    # Return updated document
    context = {
        "document": document,
    }

    context = forward(request,context,document_id)
    return render(request, "document/document.html", context)

@csrf_exempt
def transcribe_audio(request, project_id):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        #message = Message.objects.create(
        #    project_id=project_id,
        #    message=transcript["text"],
        #    user="Nico",
        #    type="audio"
        #    )
        #message.save()
        #serialized_obj = serializers.serialize('json', [message, ])
        return JsonResponse({"text":transcript["text"]}, safe=False)

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

def index(request):
    projects = Project.objects.order_by("name")
    if request.user.is_authenticated:
        projects = projects.filter(company=request.session.get("company_id"))
    records = Record.objects.all()
    context = {
        "projects": projects,
        "records": records,
    }
    return render(request, "projects/index.html", context)

def create(request, action_id:int):
    action = get_object_or_404(Action, pk=action_id)
    agent = action.agent

    # Create new document
    document = Document.objects.create(name=f"New document: {action.name}")
    document.save()

    company = get_object_or_404(Company, pk=request.session.get("company_id"))

    # Create new project
    # TODO: Name could be related to action
    project = Project.objects.create(
        name=f"New project: {action.name}",
        action=action,
        agent=agent,
        document=document,
        company=company)
    project.save()

    # Create new instruction with the selected action
    instruction = Instruction.objects.create(type=action.first_instruction_type, project=project, template=False)
    instruction.save()

    return redirect("projects:read", project_id=project.pk)

def read(request, project_id: int):
    """Read project, that is, show the main view of a project

    Args:
        request (HttpRequest): Django request object
        project_id (int): Project ID
    """

    project = get_object_or_404(Project, pk=project_id)
    document = project.document
    agent = project.agent
    action = project.action
    instructions = Instruction.objects.filter(project=project_id)
    instructions_possible = Instruction.objects.filter(type__action=action, template=True).exclude(type__in=instructions.values_list("type", flat=True))

    # Create mimesis Agent to store in session
    mms_agent = Agent(name=agent.get_name, definition=agent.get_definition)
    request.session['agent'] = mms_agent.json()
    
    context = {
        "project": project,
        "document": document,
        "instructions": instructions,
        "instructions_possible": instructions_possible,
        "agent": agent,
        "action": action
    }
    return render(request, "projects/project.html", context)

def update_name(request, project_id:int):
    project = get_object_or_404(Project, pk=project_id)
    project.name = request.POST.get("name")
    project.save()
    return JsonResponse({"name": project.name})

def delete(request, project_id:int):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect("projects:index")

@csrf_exempt
def feedback(request, project_id, document_id, instruction_id):
    print("feedback", request)
    
    # Get project
    project = get_object_or_404(Project, id=project_id)

    # Get document
    document = get_object_or_404(Document, id=document_id)
    document.clear()

    # Get instruction
    instruction = get_object_or_404(Instruction, id=instruction_id)
    
    # Remove follow-up instructions in case they existed
    Instruction.objects.filter(previous_instruction=instruction).delete()

    # Generate agent
    agent = Agent(**json.loads(request.session['agent']))
    # Create and execute selected action
    action = FeedbackGuidelines(situation=instruction.prompt)
    reply = agent.do(action)

    # Save returned
    document.text = reply
    document.create_element_from_reply(markdown=True)
    document.save()

    # Return updated document
    context = {
        "document": document,
    }
    context = forward(request,context, instruction_id)
    return render(request, "document/document.html", context)

@csrf_exempt
def feedback_values(request, project_id, document_id, instruction_id):
    print("feedback_values", request)
    context = {}

    # Generate agent
    agent = Agent(**json.loads(request.session['agent']))

    # Get instruction
    instruction = get_object_or_404(Instruction, id=instruction_id)

    # Get document
    document = get_object_or_404(Document, id=document_id)
    document.clear()

    action = FeedbackValues(feedback=document.text)
    reply = agent.do(action)

    # Save returned
    document.text = reply
    document.create_element_from_reply(markdown=True)
    document.save()

    context = {
        "document": document,
    }
    context = forward(request,context,instruction_id)
    return render(request, "document/document.html", context)