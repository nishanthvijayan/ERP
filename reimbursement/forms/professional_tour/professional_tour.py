from django import forms

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour

from reimbursement.models.professional_tour.meeting_date.meeting_date import MeetingDate


class ProfessionalTourFormForEmployee(forms.ModelForm):
    """
    ModelForm for generating fields for Professional Tour model
    """
    class Meta:
        model = ProfessionalTour
        fields = ['station_visited', 'fair_paid', 'expenditure', \
                  'purpose_visit', 'approval', 'information', 'amount_spent', \
                  'advance_taken', 'reimbursement_amount', ]

    def __init__(self, *args, **kwargs):
        super(ProfessionalTourFormForEmployee, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field].help_text
                }

    def save(self, commit=True):
        professional_tour = super(ProfessionalTourFormForEmployee, self).save(commit=False)
        if commit:
            professional_tour.save()
        return professional_tour


class ProfessionalTourFormForDA(forms.ModelForm):
    """
    ModelForm for generating fields for Professional Tour model
    """

    class Meta:
        model = ProfessionalTour
        fields = ['amount_passed', 'cheque_no']

    def __init__(self, *args, **kwargs):
        super(ProfessionalTourFormForDA, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control',
                'placeholder': self.fields[field].help_text
            }

    def save(self, commit=True):
        professional_tour = super(ProfessionalTourFormForDA, self).save(commit=False)
        if commit:
            professional_tour.save()
        return professional_tour
