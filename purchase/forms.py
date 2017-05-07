from django.forms import ModelForm, TextInput, Textarea, NumberInput

from .models import PurchaseIndentRequest


class PurchaseIndentRequestForm(ModelForm):
    class Meta:
        model = PurchaseIndentRequest
        exclude = ['indenter', 'state', 'budget_sanctioned', 'amount_already_spent', 'budget_available']

    def __init__(self, *args, **kwargs):
        super(PurchaseIndentRequestForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of the Project'})
        self.fields['budget_head'].widget = TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Budget Head (Institute, Department, Project, Others)'})
        self.fields['make_or_model_reason'].widget = Textarea(attrs={'class': 'form-control',
                                                                     'placeholder': 'Reasons why no other make or model is acceptable'})
        self.fields['proprietary_owner'].widget = TextInput(attrs={'size': '30'})
        self.fields['proprietary_distributor'].widget = TextInput(attrs={'size': '30'})


class PurchaseIndentBudgetDetailsForm(ModelForm):
    class Meta:
        model = PurchaseIndentRequest
        fields = ['budget_sanctioned', 'amount_already_spent', 'budget_available']

    def __init__(self, *args, **kwargs):
        super(PurchaseIndentBudgetDetailsForm, self).__init__(*args, **kwargs)
        self.fields['budget_sanctioned'].widget = NumberInput(attrs={'class': 'form-control', 'step': 0.01,
                                                                     'placeholder': 'Budget Sanctioned (Rs)'})
        self.fields['amount_already_spent'].widget = NumberInput(attrs={'class': 'form-control', 'step': 0.01,
                                                                        'placeholder': 'Amount already spent (Rs)'})
        self.fields['budget_available'].widget = NumberInput(attrs={'class': 'form-control', 'step': 0.01,
                                                                    'placeholder': 'Budget Available (Rs)'})
