from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from django.shortcuts import redirect

import json
from bs4 import BeautifulSoup

import markdown
import commonmark
import time

import openai

from .models import Project, Record, Message, MessageBlock#, Instruction#, Comment
from document.models import Document, DocumentElement
from actions.models import Action
from instruction.models import Instruction

from mimesis.agent.agent import Agent
from mimesis.actions.project import EvaluatePrompt, WriteProjectCharter, ReviseProjectCharter, ApplyRevisionCharter
from mimesis.actions.feedback import FeedbackGuidelines, FeedbackValues

from langchain.text_splitter import MarkdownHeaderTextSplitter

openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def actions(request, project_id):
    actions = Action.objects.all()
    context = {
        "actions": actions,
    }
    return render(request, "projects/actions.html", context)

@csrf_exempt
def select_action(request, project_id, instruction_id, action_id):
    project = get_object_or_404(Project, pk=project_id)
    instruction = get_object_or_404(Instruction, id=instruction_id)
    action = get_object_or_404(Action, id=action_id)
    instruction.action = action
    instruction.save()
    actions = Action.objects.all()
    context = {
        "project": project,
        "instruction": instruction,
        "actions": actions
    }
    return render(request, "projects/instruction.html", context)

@csrf_exempt
def instruction_update(request, project_id, instruction_id):
    print("instruction_update",request)
    project = get_object_or_404(Project, pk=project_id)
    
    # Update instruction
    instruction = get_object_or_404(Instruction, id=instruction_id)
    instruction.prompt = request.POST.get("prompt")
    instruction.finished = False
    instruction.save()

    # Delete all instructions that depend on this one
    Instruction.objects.filter(previous_instruction=instruction).delete()

    # Delete all messages that are related to this instruction
    Message.objects.filter(instruction=instruction).delete()

    # Return all instructions, so that the depencies are cleared
    instructions = Instruction.objects.filter(project=project_id)

    context = {
        "project": project,
        "document": project.document,
        "agent": project.agent,    
        "instructions": instructions,
    }
    context = forward(request, context, instruction_id)
    return render(request, "projects/instructions.html", context)

def forward(request, context, instruction_id):
    print("forward",request,context)
    forward_url = request.POST.get('forward_url')
    if forward_url:
        context["forward"] = {}
        context["forward"]["url"] = forward_url
        context["forward"]["instruction_id"] = instruction_id
        context["forward"]["target"] = request.POST.get('forward_target')
        context["forward"]["indicator"] = request.POST.get('forward_indicator')
        context["forward"]["forward"] = request.POST.get('forward_forward')
        print(context["forward"])
    return context

@csrf_exempt
def call_action(request, project_id, instruction_id, action_id):
    if request.method == 'POST':
        print("call_action", request, project_id, action_id, instruction_id)
        instruction = get_object_or_404(Instruction, id=instruction_id)
        agent = Agent(**json.loads(request.session['agent']))
        action = EvaluatePrompt(project_description=instruction.prompt)
        reply = agent.do(action)
        project = get_object_or_404(Project, pk=project_id)
        agent = get_object_or_404(Project, pk=project_id)

        enough_information = json.loads(reply)["enough_information"]
        comments = json.loads(reply)["comments"]

        if enough_information:
            message_type = "status"
        else:
            message_type = "error"

        message = Message.objects.create(
            project=project,
            message=comments,
            agent=project.agent,
            instruction=instruction,
            user="Agent",
            type=message_type
            )
        message.save()
        context = {
            "instruction": instruction,
            "reply": reply,
        }
        context = forward(request,context,instruction_id)
        return render(request, "projects/instruction.html", context)

def end_action(request, project_id, instruction_id):
    print("end_action")
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        instruction = get_object_or_404(Instruction, id=instruction_id)

        # Check if there are any follow-up actions possible
        actions = Action.objects.filter(previous_action=instruction.action)
        if actions:
            # If there are, create new empty instruction
            new_instruction = Instruction.objects.create(
                project=project,
                action=None,
                prompt=None,
                previous_instruction=instruction,
                )
            new_instruction.save()

        instruction.finished = True
        instruction.save()

        instructions = Instruction.objects.filter(project=project_id)

        context = {
            "project": project,
            "document": project.document,
            "agent": project.agent,    
            "instructions": instructions,
        }

        return render(request, "projects/instructions.html", context)

@csrf_exempt
def comment_consider(request, project_id, document_id, comment_id):
    # Get comment
    #comment = get_object_or_404(Comment, id=comment_id)
    # Set consider to True
    #comment.consider = not comment.consider
    #comment.save()
    # Return updated comment
    #context = {
    #    "comment": comment,
    #}
    context = {}
    return render(request, "projects/document_element_comment.html", context)

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
    actions = Action.objects.all()

    # Create mimesis Agent to store in session
    mms_agent = Agent(name=agent.name, definition=agent.definition)
    request.session['agent'] = mms_agent.json()
    
    messages = Message.objects.filter(project=project_id, type="audio")
    context = {
        "project": project,
        "document": document,
        "instructions": instructions,
        "agent": agent,
        "actions": actions
    }
    return render(request, "projects/project.html", context)

def new(request, action_id:int):
    action = get_object_or_404(Action, pk=action_id)
    agent = action.agent

    # Create new document
    document = Document.objects.create(name="New document")
    document.save()

    # Create new project
    project = Project.objects.create(name="New project", agent=agent, document=document) # TODO: Name could be related to action
    project.save()

    # Create new instruction with the selected action
    instruction = Instruction.objects.create(project=project, action=action)
    instruction.save()

    instructions = Instruction.objects.filter(project=project.pk)

    context = {
        "project": project,
        "document": document,
        "instructions": instructions,
        "agent": agent,
        "actions": actions
    }
    return redirect("projects:project", project_id=project.pk)
    #return render(request, "projects/project.html", context)

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

    time.sleep(2)

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