# Signals
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import Profile

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    print("user_signed_up_")
    profile = Profile(user=user)
    profile.save()
    user.save()