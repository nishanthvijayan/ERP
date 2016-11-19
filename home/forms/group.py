from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import Group

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['permissions']
    def __init__(self, *args, **kwargs):
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})

class EditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        exclude = ['permissions']

    def __init__(self, *args, **kwargs):
        super(EditGroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
