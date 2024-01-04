# app/signals/handlers.py
from django.db.models import Q
from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from user.models import Profile
from company.models import Company

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    # Obtén el subdominio
    subdomain = request.META['HTTP_HOST'].split('.')[0]

    # Prefetch las compañías con el subdominio dado o con id=2
    companies = Company.objects.filter(Q(subdomain=subdomain) | Q(id=2))

    # Obtén la compañía con el subdominio dado, o la compañía con id=2 si no se encuentra ninguna compañía con el subdominio dado
    company = companies.filter(subdomain=subdomain).first() or companies.get(id=2)

    # Obtén el grupo con el nombre 'company_user_default'
    group = Group.objects.get(name='company_user_default')

    # Añade el grupo al usuario
    user.groups.add(group)

    # Crea el perfil del usuario
    profile = Profile.objects.create(user=user)

    # Añade la compañía al perfil
    profile.companies.add(company)