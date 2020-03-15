from django import forms
from main_project.models import File,UserFile


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        widgets = {
            'expiration_date': forms.DateInput(attrs={'class':'datepicker'}),
        }
        fields = ('name', 'description','expiration_date','file',)
