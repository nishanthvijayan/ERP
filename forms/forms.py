from django.forms import Form, ModelForm
from .models import Workflow, FormElement, State, Transition

class WorkflowForm(ModelForm):
    class Meta:
        model = Workflow
        fields = '__all__'

class FormElementForm(ModelForm):
    class Meta:
        model = FormElement
        exclude = ['workflow']

class StateForm(ModelForm):
    class Meta:
        model = State
        exclude = ['workflow']

class TransitionForm(ModelForm):
    class Meta:
        model = Transition
        exclude = ['workflow']