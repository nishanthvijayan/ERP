from django import forms

from reimbursement.models.medical.amount_detail import AmountDetail


class AmountDetailForm(forms.ModelForm):
    """
    ModelForm for generating fields for AmountDetail model
    """
    class Meta:
        model = AmountDetail
        fields = [
            'amount_passed_medicine', 'amount_passed_test', 'amount_passed_room_rent',
            'amount_passed_other', 'medical_reimbursement_register_page_no',
            'medical_reimbursement_register_sr_no'
        ]

    def __init__(self, *args, **kwargs):
        super(AmountDetailForm, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field].help_text
                }

    def save(self, commit=True):
        amount_detail = super(AmountDetailForm, self).save(commit=False)
        if commit:
            amount_detail.save()
        return amount_detail


class AmountDetailFormForEmployee(forms.ModelForm):
    """
    ModelForm for generating fields that's value has to be entered by employee for AmountDetail model
    """
    class Meta:
        model = AmountDetail
        fields = ['amount_claimed_test',
                  'amount_claimed_room_rent',
                  'amount_claimed_other'
        ]

    def __init__(self, *args, **kwargs):
        super(AmountDetailFormForEmployee, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field].help_text
                }

    def save(self, commit=True):
        amount_detail = super(AmountDetailFormForEmployee, self).save(commit=False)
        if commit:
            amount_detail.save()
        return amount_detail
