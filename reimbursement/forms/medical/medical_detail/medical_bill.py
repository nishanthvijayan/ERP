from django import forms

from reimbursement.models.medical.medical_detail import MedicalBill


class MedicalBillForm(forms.ModelForm):
    class Meta:
        model = MedicalBill
        exclude = ['medical']

    def __init__(self, *args, **kwargs):
        super(MedicalBillForm, self).__init__(*args, **kwargs)
        self.fields['image_file'].widget.attrs = {
                        'class': 'form-control',
                        'placeholder': self.fields['image_file'].help_text
                    }

    def save(self, commit=True):
        medical_detail = super(MedicalBillForm, self).save(commit=False)
        if commit:
            medical_detail.save()
        return medical_detail
