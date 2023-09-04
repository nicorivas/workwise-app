from django import forms

from .models import ActionElement, ActionElementAgentCall

class ActionElementCreateForm(forms.ModelForm):
    class Meta:
        model = ActionElement
        fields = ["type", "name"]

class ActionElementUpdateForm(forms.ModelForm):
    class Meta:
        model = ActionElement
        fields = ["name","guide","index"]

class AgentCallUpdateForm(forms.ModelForm):
    class Meta:
        model = ActionElementAgentCall
        fields = ["name","button_label","index","mimesis_action","document_input"]