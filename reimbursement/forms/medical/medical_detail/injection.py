from django import forms

from reimbursement.models.medical.medical_detail.injection import Injection


class InjectionForm(forms.ModelForm):
    class Meta:
        model = Injection
        exclude = ['medical_detail']

    def __init__(self, *args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)
        for field in Injection._meta.get_fields():
            if field.name in self.fields:
                self.fields[field.name].widget.attrs = {
                        'class': 'form-control',
                        'placeholder': self.fields[field.name].help_text
                    }

    def save(self, commit=True):
        injection = super(InjectionForm, self).save(commit=False)
        if commit:
            injection.save()
        return injection
