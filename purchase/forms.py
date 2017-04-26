from django.forms import ModelForm, TextInput, Textarea, NumberInput

from .models import PurchaseIndentRequest


class PurchaseIndentRequestForm(ModelForm):
    class Meta:
        model = PurchaseIndentRequest
        exclude = ['indenter', 'state', 'budget_sanctioned', 'amount_already_spent', 'budget_available']

    def __init__(self, *args, **kwargs):
        super(PurchaseIndentRequestForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['budget_head'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['make_or_model_reason'].widget = Textarea(attrs={'class': 'form-control'})


class PurchaseIndentBudgetDetailsForm(ModelForm):
    class Meta:
        model = PurchaseIndentRequest
        fields = ['budget_sanctioned', 'amount_already_spent', 'budget_available']

    def __init__(self, *args, **kwargs):
        super(PurchaseIndentBudgetDetailsForm, self).__init__(*args, **kwargs)
        self.fields['budget_sanctioned'].widget = NumberInput(attrs={'class': 'form-control', 'step': 0.01})
        self.fields['amount_already_spent'].widget = NumberInput(attrs={'class': 'form-control', 'step': 0.01})
        self.fields['budget_available'].widget = NumberInput(attrs={'class': 'form-control', 'step': 0.01})
