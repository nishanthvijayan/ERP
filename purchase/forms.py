from django.forms import Form, ModelForm, TextInput, Textarea, NumberInput, \
    CharField, IntegerField, Select, ChoiceField, DecimalField, EmailField, EmailInput

from .models import PurchaseIndentRequest


class PurchaseIndentRequestForm(ModelForm):
    class Meta:
        model = PurchaseIndentRequest
        exclude = ['indenter', 'state', 'budget_sanctioned', 'amount_already_spent', 'budget_available']

    def __init__(self, *args, **kwargs):
        super(PurchaseIndentRequestForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].widget = TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Name of the Project'
        })
        AVAILABLE_HEADS = (
            ('Institute', 'Institute'),
            ('Department', 'Department'),
            ('Project', 'Project'),
            ('Others', 'Others'),
        )
        self.fields['budget_head'].widget = Select(attrs={'class': 'form-control'}, choices=AVAILABLE_HEADS)
        AVAILABLE_CATEGORIES = (
            ('Non Recurring', 'Non Recurring'),
            ('Recurring', 'Recurring'),
            ('Others', 'Others'),
        )
        self.fields['category'].widget = Select(attrs={'class': 'form-control'}, choices=AVAILABLE_CATEGORIES)
        self.fields['make_or_model_reason'].widget = Textarea(attrs={
            'class': 'form-control', 'placeholder': 'Reasons why no other make or model is acceptable'
        })
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


class ItemVendorForm(Form):
    specification = CharField(
        max_length=1000,
        widget=Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Specification of Item',
            'rows': '3'
        }), required=True)
    quantity = IntegerField(
        widget=NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantity required',
        }), required=True)
    estimated_cost = DecimalField(
        widget=NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estimated Cost (Rs)',
            'step': 0.01
        }), required=True)
    AVAILABLE_TYPES = (
        ('Lab Consumables', 'Lab Consumables'),
        ('General Items', 'General Items'),
        ('Lab Equipment(s)', 'Lab Equipment(s)'),
        ('Office Equipment(s)', 'Office Equipment(s)'),
        ('Lab Furniture', 'Lab Furniture'),
        ('Office Furniture', 'Office Furniture')
    )
    type = ChoiceField(widget=Select(attrs={'class': 'form-control'}), choices=AVAILABLE_TYPES)

    vendor_name = CharField(
        max_length=100,
        widget=TextInput(attrs={'placeholder': 'Name of Vendor', 'class': 'form-control'}),
        required=True
    )

    vendor_address = CharField(
        max_length=500,
        widget=Textarea(attrs={'placeholder': 'Address', 'rows': '2', 'class': 'form-control'}),
        required=True
    )

    vendor_email = EmailField(
        max_length=50,
        widget=EmailInput(attrs={'placeholder': 'Email Address of Vendor', 'class': 'form-control'}),
        required=False
    )
