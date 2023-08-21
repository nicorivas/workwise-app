from django import forms

from .models import InstructionType

class InstructionTypeCreateForm(forms.ModelForm):
    class Meta:
        model = InstructionType
        fields = ["name", "action"]