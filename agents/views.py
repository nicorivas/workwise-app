import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader

from .models import Agent
from actions.models import Action
from projects.models import Project

def index(request):
    agents = Agent.objects.order_by("name")
    output = ", ".join([q.get_name for q in agents])

    template = loader.get_template("agents/index.html")
    context = {
        "agents": agents,
    }
    if request.POST.get("source") == "menu":
        return render(request, "agents/main.html", context)
    else:
        return render(request, "agents/index.html", context)

def check_project(request, agent_id, project_id):

        print("check_project")

        agent = get_object_or_404(Agent, pk=agent_id)
        project = get_object_or_404(Project, pk=project_id)

        if agent.check_project(project):
            return HttpResponse("Project checked!")
        else:
            return HttpResponse("Project not checked!")

def detail(request, agent_id):

    agent = get_object_or_404(Agent, pk=agent_id)
    return render(request, "agents/detail.html", {"agent": agent})

def search_action_guide(request, agent_id, action_id):
    print("search_action_guide")
    agent = get_object_or_404(Agent, pk=agent_id)
    action = get_object_or_404(Action, pk=action_id)
    search_query = request.POST.get("query")
    prompt = f"""Act as if you're an {agent.get_short_title} agent. You are part of a company.
                         
                         Someone on the company just asked you a question: {search_query}.

                         You just recommended this person that he should do this action: {action.name}.

                         Could you briefly reply why do you think this action could help this person?
                         Please make it very short, no more than two sentences.
                         Please reply as if you are talking to the person who asked the question.
                         """
    print(prompt)
    agent.stream_prompt(request, prompt, fast=True)
    return JsonResponse({})