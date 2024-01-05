from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CustomSignupForm(SignupForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email
