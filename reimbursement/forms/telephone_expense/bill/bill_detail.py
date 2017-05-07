from django import forms

from reimbursement.models.telephone_expense.bill.bill_detail import BillDetail


class BillDetailForm(forms.ModelForm):
    class Meta:
        model = BillDetail
        exclude = ['telephone_expense']

    def __init__(self, *args, **kwargs):
        super(BillDetailForm, self).__init__(*args, **kwargs)
        for field in BillDetail._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                        'class': 'form-control',
                        'placeholder': self.fields[field.name].help_text
                    }
                self.fields['is_telephone_line'].widget.attrs = {
                    'class': ''
                }

    def save(self, commit=True):
        bill_detail = super(BillDetailForm, self).save(commit=False)
        if commit:
            bill_detail.save()
        return bill_detail
