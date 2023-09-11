from django.shortcuts import render

from agents.models import Agent
from actions.models import Action
from django.shortcuts import redirect

def action_select(request, action_id:int):
    return redirect("projects:project",1)

def index(request):
    agents = Agent.objects.filter(show_in_explorer=True)
    actions = Action.objects.all()
    context = {
        "actions": actions,
        "agents": agents
        }
    return render(request, "explorer/index.html", context)