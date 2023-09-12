from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from company.models import Company


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
    return render(request, "header_company.html", context)