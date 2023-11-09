# app/signals/handlers.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group

from user.models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, created, **kwargs):

    if created:
        g1 = Group.objects.get(name='company_user_default')
        instance.groups.add(g1)
        instance.save()

        # Create user profile
        profile = Profile.objects.create(user=instance)
        profile.companies.add(3)
        profile.save()