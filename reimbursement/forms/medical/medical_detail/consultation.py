from django import forms

from reimbursement.models.medical.medical_detail.consultation import Consultation


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        exclude = ['medical_detail']

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
        for field in Consultation._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field.name].help_text
                }

    def save(self, commit=True):
        consultation = super(ConsultationForm, self).save(commit=False)
        if commit:
            consultation.save()
        return consultation
