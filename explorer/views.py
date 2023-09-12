from django.shortcuts import render
from django.shortcuts import get_object_or_404

from agents.models import Agent
from actions.models import Action
from company.models import Company

def index(request):
    agents = Agent.objects.filter(show_in_explorer=True)
    # If we are part of a company, then filter by company
    company_id = request.session.get("company_id")
    if company_id:
        company = get_object_or_404(Company, pk=company_id)
        agents = agents.filter(company=company)
    else:
        if request.user.is_authenticated:
            company = request.user.profile.companies.first()
            if company:
                agents = agents.filter(company=company)
                request.session["company_id"] = company.pk
    actions = Action.objects.all()
    context = {
        "actions": actions,
        "agents": agents
        }
    return render(request, "explorer/index.html", context)