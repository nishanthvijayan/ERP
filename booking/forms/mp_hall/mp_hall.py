from django import forms

from booking.models.mp_hall.mp_hall import MpHall


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

    def save(self, commit=True):
        booking_detail = super(MpHallForm, self).save(commit=False)
        if commit:
            booking_detail.save()
        return booking_detail
