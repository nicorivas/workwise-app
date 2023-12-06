from django import forms

from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "action", "project"]

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        # Iterate over fields an add form-control class
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})