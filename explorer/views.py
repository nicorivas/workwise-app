from django.shortcuts import render
from django.shortcuts import get_object_or_404

from agents.models import Agent
from actions.models import Action
from company.models import Company

def index(request):
    company_id = request.session.get("company_id")
    company = get_object_or_404(Company, pk=company_id)
    agents = Agent.objects.filter(show_in_explorer=True, company=company)
    actions = Action.objects.all()
    context = {
        "actions": actions,
        "agents": agents
        }
    return render(request, "explorer/index.html", context)