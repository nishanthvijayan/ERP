from django.forms import Form, ModelForm, TextInput, Select
from .models import Workflow, FormElement, State, Transition

class WorkflowForm(ModelForm):
    class Meta:
        model = Workflow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WorkflowForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['description'].widget = TextInput(attrs={'class': 'form-control'})

class FormElementForm(ModelForm):
    class Meta:
        model = FormElement
        exclude = ['workflow']

    def __init__(self, *args, **kwargs):
        super(FormElementForm, self).__init__(*args, **kwargs)
        AVAILABLE_ELEMENT_TYPES = (
        ('text_input', 'Text Input'),
        ('number_input', 'Number Input'),
        ('option_group', 'Option Group'),
        ('text_area', 'Text Area'))
        self.fields['caption'].widget = TextInput(attrs={'class': 'form-control','required': True})
        self.fields['hint'].widget = TextInput(attrs={'class': 'form-control','required': True})
        self.fields['element_type'].widget = Select(attrs={'class': 'form-control','required': True}, choices=AVAILABLE_ELEMENT_TYPES)
        self.fields['position'].widget = TextInput(attrs={'type':'number','class': 'form-control','required': True })

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
        ('Rejected', 'Rejected'))
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control','required': True})
        self.fields['kind'].widget = Select(attrs={'class': 'form-control','required': True}, choices=AVAILABLE_KINDS)

class TransitionForm(ModelForm):
    class Meta:
        model = Transition
        exclude = ['workflow']

    def __init__(self, *args, **kwargs):
        super(TransitionForm, self).__init__(*args, **kwargs)
        self.fields['from_state'].widget = Select(attrs={'class': 'form-control','required': True})
        self.fields['to_state'].widget = Select(attrs={'class': 'form-control','required': True})
        self.fields['allowed_groups'].widget = Select(attrs={'class': 'form-control','required': True,'multiple': 'multiple'})
