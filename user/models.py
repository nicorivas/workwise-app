from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from agents.models import Agent

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_pictures", default="profile_pictures/default.png", null=True, blank=True)
    # Companies a user is part of
    companies = models.ManyToManyField(Company, blank=True)
    # Agents that the user has access to
    agents = models.ManyToManyField(Agent, blank=True)

    @property
    def get_name(self):
        if self.user.first_name:
            return self.user.first_name + " " + self.user.last_name
        else:
            return self.user.username

    def __str__(self):
        return self.user.username