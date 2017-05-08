from django import forms

from reimbursement.models.medical.medical_detail.medicine import Medicine


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        exclude = ['medical_detail']

    def __init__(self, *args, **kwargs):
        super(MedicineForm, self).__init__(*args, **kwargs)
        for field in Medicine._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                        'class': 'form-control',
                        'placeholder': self.fields[field.name].help_text
                    }

    def save(self, commit=True):
        medicine = super(MedicineForm, self).save(commit=False)
        if commit:
            medicine.save()
        return medicine
