from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from agents.models import Agent

from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

from invitations.app_settings import app_settings
from invitations.base_invitation import AbstractBaseInvitation

class CompanyUserInvitation(AbstractBaseInvitation):
    
    email = models.EmailField(unique=True, verbose_name=_('e-mail address'), max_length=app_settings.EMAIL_MAX_LENGTH)
    created = models.DateTimeField(verbose_name=_('created'), default=timezone.now)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)

    @classmethod
    def create(cls, email, inviter=None, company=None,  **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key,
            inviter=inviter,
            company=company,
            **kwargs)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = kwargs.pop('site', Site.objects.get_current())
        invite_url = reverse(app_settings.CONFIRMATION_URL_NAME, args=[self.key])                                                                                                                                                                        
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update({
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
        })

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Full name
    full_name = models.CharField(max_length=256, null=True, blank=True)
    # Profile picture
    picture = models.ImageField(upload_to="profile_pictures", default="profile_pictures/default.png", null=True, blank=True)
    # Companies a user is part of
    companies = models.ManyToManyField(Company, blank=True, default=3)
    # Agents that the user has access to
    agents = models.ManyToManyField(Agent, blank=True)
    # If the user is part of beta features
    beta = models.BooleanField(default=False)
    # If the user can see alpha features
    alpha = models.BooleanField(default=False)
    
    @property
    def get_name(self):
        if self.user.first_name:
            return self.user.first_name + " " + self.user.last_name
        else:
            return self.user.username

    def __str__(self):
        return self.user.username