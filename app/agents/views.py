from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import AgentDB

def index(request):
    agents = AgentDB.objects.order_by("name")
    output = ", ".join([q.name for q in agents])

    template = loader.get_template("agents/index.html")
    context = {
        "agents": agents,
    }
    return render(request, "agents/index.html", context)

def detail(request, agent_id):

    agent = get_object_or_404(AgentDB, pk=agent_id)
    return render(request, "agents/detail.html", {"agent": agent})