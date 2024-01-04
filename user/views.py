from django.contrib.auth.models import User
from django.views import View
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .api import UserSerializerNormal
from company.models import Company


class UserCreateView(View):

    def post(self, request, company_id=None):

        host = request.get_host()
        subdomain = host.split('.')[0]

        user, created = User.objects.get_or_create(email=request.POST.get('email'), username=request.POST.get('email'))
        if (created):
            user.first_name = request.POST.get('name')
        
         # Intentar asignar la compañía basada en el subdominio
        try:
            company = Company.objects.get(name=subdomain)
            user.profile.companies.add(company)
        except Company.DoesNotExist:
            # Si la compañía basada en el subdominio no existe, usar el parámetro GET
            if request.POST.get("company"):
                user.profile.companies.add(request.POST.get("company"))

        user.save()

        return JsonResponse(UserSerializerNormal(user).data)
    
user_create_view = UserCreateView.as_view()