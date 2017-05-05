from django import forms

from reimbursement.models.medical.general_detail import GeneralDetail


class GeneralDetailForm(forms.ModelForm):
    class Meta:
        model = GeneralDetail
        fields = ['patient_name','patient_age','employee_relationship']

    def __init__(self, *args, **kwargs):
        super(GeneralDetailForm, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field].help_text
                }

    def save(self, commit=True):
        general_detail = super(GeneralDetailForm, self).save(commit=False)
        if commit:
            general_detail.save()
        return general_detail
