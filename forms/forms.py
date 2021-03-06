from django.forms import ModelForm, TextInput, Select, ModelChoiceField, ModelMultipleChoiceField, SelectMultiple
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from .models import Workflow, FormElement, State, Transition


class WorkflowForm(ModelForm):
    class Meta:
        model = Workflow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WorkflowForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['description'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['description'].required = False
        self.fields['allowed_groups'] = ModelMultipleChoiceField(queryset=Group.objects.all(
            ), widget=SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}))


class FormElementForm(ModelForm):
    class Meta:
        model = FormElement
        exclude = ['workflow']

    def __init__(self, *args, **kwargs):
        super(FormElementForm, self).__init__(*args, **kwargs)
        AVAILABLE_ELEMENT_TYPES = (
            ('text_input', 'Text Input'),
            ('number_input', 'Number Input'),
            ('date_input', 'Date Input'),
            ('time_input', 'Time Input'),
            ('date_time_input', 'Date Time Input'),
            ('text_area', 'Text Area')
        )
        self.fields['caption'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['hint'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['hint'].required = False
        self.fields['element_type'].widget = Select(attrs={'class': 'form-control'}, choices=AVAILABLE_ELEMENT_TYPES)
        self.fields['position'].widget = TextInput(attrs={'type': 'number', 'class': 'form-control'})


class StateForm(ModelForm):
    class Meta:
        model = State
        exclude = ['workflow']

    def __init__(self, *args, **kwargs):
        super(StateForm, self).__init__(*args, **kwargs)
        AVAILABLE_KINDS = (
            ('Initial', 'Initial'),
            ('Intermediate', 'Intermediate'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected')
        )
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['kind'].widget = Select(attrs={'class': 'form-control'}, choices=AVAILABLE_KINDS)
        self.fields['allowed_groups'] = ModelMultipleChoiceField(queryset=Group.objects.all(
            ), widget=SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}))


class TransitionForm(ModelForm):
    class Meta:
        model = Transition
        exclude = ['workflow']

    def __init__(self, *args, **kwargs):
        workflow = get_object_or_404(Workflow, pk=int(kwargs.pop('workflow_id')))
        super(TransitionForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['from_state'] = ModelChoiceField(
            queryset=workflow.state_set.all(), widget=Select(attrs={'class': 'form-control'}))
        self.fields['to_state'] = ModelChoiceField(
            queryset=workflow.state_set.all(), widget=Select(attrs={'class': 'form-control'}))
