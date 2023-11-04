import json

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from document.models import Document
from company.models import Company
from instruction.models import Instruction

def main(request):
    return render(request, "body.html")

def test(request):
    return render(request, "test.html")

def logout_view(request):
    logout(request)
    return redirect("explorer:index")

def header_company(request):
    # Get company id from session.
    # If there is no session info, then set to first company and save session,.
    if request.user.is_authenticated:
        company_id = request.session.get("company_id")
        if company_id:
            company = get_object_or_404(Company, pk=company_id)
        else:
            company = request.user.profile.companies.first()
            request.session["company_id"] = company.pk
    else:
        company = None

    context = {"company": company}
    return render(request, "body_header_company.html", context)

def component(request, component):
    context = {"component": component}
    if component == "selector":
        context["items"] = Document.objects.all()[:5]
    if component == "chips":
        context["items"] = Document.objects.all()[:5]
    if component == "button":
        context["label"] = "Test button"
    if component == "dropdown":
        context["items"] = Document.objects.all()[:5]
    if component == "instruction":
        context["instruction"] = Instruction.objects.get(pk=327)
    if component == "document":
        context["document"] = Document.objects.get(pk=232)
    if component == "radioButtons":
        context["items"] = Document.objects.all()[:5]
    return render(request, "components/view.html", context)

def socket_test(request):
    return render(request, "app/socket_test.html")