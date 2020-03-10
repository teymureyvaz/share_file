from django import forms
from main_project.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'description','expiration_date','file',)