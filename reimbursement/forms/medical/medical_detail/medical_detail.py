from django import forms

from reimbursement.models.medical.medical_detail import MedicalDetail


class MedicalDetailForm(forms.ModelForm):
    class Meta:
        model = MedicalDetail
        exclude = ['medical', 'total_amount_claimed']

    def __init__(self, *args, **kwargs):
        super(MedicalDetailForm, self).__init__(*args, **kwargs)
        for field in MedicalDetail._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                        'class': 'form-control',
                        'placeholder': self.fields[field.name].help_text
                    }

    def save(self, commit=True):
        medical_detail = super(MedicalDetailForm, self).save(commit=False)
        if commit:
            medical_detail.save()
        return medical_detail
