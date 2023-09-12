from django.db import models
from django.contrib.auth.models import User
from company.models import Company

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    companies = models.ManyToManyField(Company, null=True, blank=True)