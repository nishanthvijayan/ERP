from django import forms

from reimbursement.models.professional_tour.meeting_date.meeting_date import MeetingDate


class MeetingDateFormForEmployee(forms.ModelForm):
    """
    ModelForm for generating fields for Professional Tour model
    """
    class Meta:
        model = MeetingDate
        fields = ['meeting_date' ]

    def __init__(self, *args, **kwargs):
        super(MeetingDateFormForEmployee, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field].help_text
                }

    def save(self, commit=True):
        meeting_date = super(MeetingDateFormForEmployee, self).save(commit=False)
        if commit:
            meeting_date.save()
        return meeting_date