from django.shortcuts import render

from agents.models import AgentDB
from actions.models import ActionDB

def index(request):
    agents = AgentDB.objects.all()
    actions = ActionDB.objects.all()
    context = {
        "actions": actions,
        "agents": agents
        }
    return render(request, "explorer/index.html", context)