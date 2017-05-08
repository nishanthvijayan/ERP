from django import forms

from booking.models.mp_hall.mp_hall import MpHall

import datetime


class MpHallForm(forms.ModelForm):
    """
    ModelForm for generating fields for AmountDetail model
    """
    class Meta:
        model = MpHall
        fields = ['date', 'from_time', 'to_time', \
                  'purpose', 'laptop_req', 'projector_req', 'audio_req', \
                  'video_req']

    def __init__(self, *args, **kwargs):
        super(MpHallForm, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs = {
                    'class': 'form-control',
                    'placeholder': self.fields[field].help_text
                }
        self.fields['date'].widget.attrs = {
            'data-provide':'datepicker',
            'class': 'form-control',
            'placeholder': self.fields['date'].help_text
        }

    def clean(self):
        """
        This method overrides the default clean method of BaseModel.Model.
        This function add extra functionality that checks
         > if diagnosis_advised is true than certificate image must be uploaded
        :return:
        """
        current_date = datetime.date.today().strftime("%Y-%m-%d")

        if self.cleaned_data['date'].strftime("%Y-%m-%d") < current_date:
            raise forms.ValidationError('Error in booking date !!')
        if self.cleaned_data['from_time'] > self.cleaned_data['to_time']:
            raise forms.ValidationError('Error in booking timings !!')


    def save(self, commit=True):
        booking_detail = super(MpHallForm, self).save(commit=False)
        if commit:
            booking_detail.save()
        return booking_detail
