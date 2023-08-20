from django.shortcuts import render
from django.views import View
from django.shortcuts import render, get_object_or_404

from .models import Company

class CompanyView(View):
    
    def get(self, request, company_id):
        print("CompanyView.get")
        company = get_object_or_404(Company, pk=company_id)
        context = {
            "company": company,
        }
        return render(request, "company/index.html", context)
    
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