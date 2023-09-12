from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from company.models import Company


def logout_view(request):
    logout(request)
    return redirect("explorer:index")

def header_company(request):
    company_id = request.session.get("company_id")
    company = get_object_or_404(Company, pk=company_id)
    context = {"company": company}
    return render(request, "header_company.html", context)