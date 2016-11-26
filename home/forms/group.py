from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import Group


class GroupForm(forms.ModelForm):

    '''
    Generates Model Form to create Group and update Group info.
    '''

    class Meta:
        model = Group
        exclude = ['permissions']

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(
            attrs={'class': 'form-control'})
