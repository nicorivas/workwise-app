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
        fields = ["author_name", "author_email", "startup_name", "startup_level", "pitch", "pitch_analysis_short"]
        labels = {
            'author_name': 'Nombre',
            'author_email': 'Correo electrónico',
            'startup_name': 'Nombre de la Startup',
            'startup_level': 'Madurez de la Startup',
            'pitch': 'Pitch',
            'pitch_analysis_short': 'Análisis',
        }
        widgets = {
            'startup_level': forms.RadioSelect(),
        }

class FlowRegisterForm(forms.Form):

    author_name = forms.CharField(label="Nombre", max_length=100, required=True)
    author_email = forms.EmailField(label="Correo", max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix