from django import forms
from django.forms import ChoiceField

from mimesis.library.library import Library

from .models.instruction import InstructionType

class InstructionTypeCreateForm(forms.ModelForm):
    class Meta:
        model = InstructionType
        fields = ["name", "action"]

class InstructionTypeUpdateForm(forms.ModelForm):
    class Meta:
        model = InstructionType
        fields = ["name", "action"]

from .models.instruction import Instruction

class InstructionUpdateForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ["type"]

from .models.instruction_element import InstructionElement, InstructionElementMessage, InstructionElementTextInput, InstructionElementAgentCall

class InstructionElementCreateForm(forms.ModelForm):
    class Meta:
        model = InstructionElement
        fields = ["type", "name"]

class InstructionElementUpdateForm(forms.ModelForm):
    class Meta:
        model = InstructionElement
        fields = ["name","guide","index"]

class InstructionElementMessageUpdateForm(forms.ModelForm):
    class Meta:
        model = InstructionElementMessage
        fields = ["message"]

class InstructionElementTextInputUpdateForm(forms.ModelForm):
    class Meta:
        model = InstructionElementTextInput
        fields = ["message", "audio"]

class InstructionElementAgentCallUpdateForm(forms.ModelForm):

    mimesis_action = ChoiceField(choices=Library.get_all())

    class Meta:
        model = InstructionElementAgentCall
        fields = ["name","button_label","index","mimesis_action","document_input"]

    def __init__(self, *args, **kwargs):
            """
            We do this to reload the choices everytime the form is loaded.
            """
            super(InstructionElementAgentCallUpdateForm, self).__init__(*args, **kwargs)     
            self.fields['mimesis_action'] = ChoiceField(choices=Library.get_all())