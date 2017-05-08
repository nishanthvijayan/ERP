from django import forms

from reimbursement.models.medical.medical_detail.specialist_consultation import SpecialistConsultation


class SpecialistConsultationForm(forms.ModelForm):
    class Meta:
        model = SpecialistConsultation
        exclude = ['medical_detail']

    def __init__(self, *args, **kwargs):
        super(SpecialistConsultationForm, self).__init__(*args, **kwargs)
        for field in SpecialistConsultation._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field.name].help_text
                }

    def save(self, commit=True):
        specialist_consultation = super(SpecialistConsultationForm, self).save(commit=False)
        if commit:
            specialist_consultation.save()
        return specialist_consultation
