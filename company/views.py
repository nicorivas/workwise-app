from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from .models import Company

class CompanyView(View):
    
    def get(self, request, company_id):
        print("CompanyView.get")
        company = get_object_or_404(Company, pk=company_id)
        context = {
            "company": company,
        }
        return render(request, "company/index.html", context)

class CompanySetView(View):
    
    def post(self, request, company_id):
        request.session["company_id"] = company_id
        response = HttpResponse()
        response["HX-Redirect"] = reverse("explorer:index")
        return response

class CompanyStrategyView(View):
    
    def get(self, request, company_id):
        print("CompanyStrategy.get")
        company = get_object_or_404(Company, pk=company_id)
        context = {
            "company": company,
        }
        return render(request, "company/strategy.html", context)
    
class CompanyValuesView(View):
    
    def get(self, request, company_id):
        print("CompanyValues.get")
        company = get_object_or_404(Company, pk=company_id)
        context = {
            "company": company,
        }
        return render(request, "company/values.html", context)