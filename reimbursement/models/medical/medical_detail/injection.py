from django.db import models

from erp_core.models import BaseModel

from medical_detail import MedicalDetail


class Injection(BaseModel):
    """
    This stores date and fee for consultation regarding employee health
    """
    date = models.DateField(
        help_text='Injection Date'
    )
    fee = models.PositiveIntegerField(
        help_text='Injection Fee'
    )
    medical_detail = models.ForeignKey(
        MedicalDetail,
        on_delete=models.CASCADE,
        help_text='Medical detail id'
    )

    def __str__(self):
        return str(self.date)

    def __unicode__(self):
        return str(self.date)
