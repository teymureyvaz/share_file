from django import forms
from main_project.models import File,UserFile


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('name', 'description','expiration_date','file',)
