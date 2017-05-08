from django import forms

from reimbursement.models.telephone_expense.bill.bill_image import BillImage


class BillImageForm(forms.ModelForm):
    class Meta:
        model = BillImage
        exclude = ['telephone_expense']

    def __init__(self, *args, **kwargs):
        super(BillImageForm, self).__init__(*args, **kwargs)
        for field in BillImage._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                        'class': 'form-control',
                        'placeholder': self.fields[field.name].help_text
                    }

    def save(self, commit=True):
        bill_image = super(BillImageForm, self).save(commit=False)
        if commit:
            bill_image.save()
        return bill_image
