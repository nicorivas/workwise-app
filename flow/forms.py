from django import forms
from django.forms import ChoiceField
from .models import *


class PitchCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author_name'].widget.attrs['placeholder'] = "Nicolás Rivas"
        self.fields['author_email'].widget.attrs['placeholder'] = "nico@getworkwise.ai"
        self.fields['startup_name'].widget.attrs['placeholder'] = "WorkWise"
        self.label_suffix = ""  # Removes : as label suffix
        
    class Meta:
        model = Pitch
        fields = ["author_name", "author_email", "startup_name", "startup_level"]
        labels = {
            'author_name': 'Nombre',
            'author_email': 'Correo electrónico',
            'startup_name': 'Nombre de la Startup',
            'startup_level': 'Madurez de la Startup',
        }