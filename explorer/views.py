from django.shortcuts import render

from agents.models import AgentDB
from actions.models import Action
from django.shortcuts import redirect

def action_select(request, action_id:int):
    print("action_select")
    return redirect("projects:project",1)

def index(request):
    agents = AgentDB.objects.all()
    actions = Action.objects.all()
    context = {
        "actions": actions,
        "agents": agents
        }
    return render(request, "explorer/index.html", context)