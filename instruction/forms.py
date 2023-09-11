from django import forms

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

from .models.instruction_element import InstructionElement, InstructionElementMessage, InstructionElementAgentCall

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

class InstructionElementAgentCallUpdateForm(forms.ModelForm):
    class Meta:
        model = InstructionElementAgentCall
        fields = ["name","button_label","index","mimesis_action","document_input"]