from django import forms

class LoaderGoogleDocsForm(forms.Form):
    document_id = forms.CharField(label="Document ID", max_length=100)