from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Agent
from projects.models import Project

def index(request):
    agents = Agent.objects.order_by("name")
    output = ", ".join([q.get_name for q in agents])

    template = loader.get_template("agents/index.html")
    context = {
        "agents": agents,
    }
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