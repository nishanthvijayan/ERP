from django.db import models

from erp_core.models import BaseModel

from medical_detail import MedicalDetail


class Consultation(BaseModel):
    """
    This stores date and fee for consultation regarding employee health
    """
    date = models.DateField(
        help_text='Consultation Date'
    )
    fee = models.PositiveIntegerField(
        help_text='Consultation Fee'
    )
    medical_detail = models.ForeignKey(
        MedicalDetail,
        on_delete=models.CASCADE,
        related_name='consultation',
        help_text='Medical detail id'
    )

    def __str__(self):
        return str(self.date)

    def __unicode__(self):
        return str(self.date)
