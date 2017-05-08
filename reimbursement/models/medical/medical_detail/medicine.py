from django.db import models

from erp_core.models import BaseModel

from medical_detail import MedicalDetail


class Medicine(BaseModel):
    """
    This stores name of medicine and its price and the MedicalDetail its associated to.
    """
    name = models.CharField(
        max_length=200,
        help_text='Name of the medicine'
    )
    # What should be the max price for the medicines ?
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price of the medicine'
    )
    medical_detail = models.ForeignKey(
        MedicalDetail,
        on_delete=models.CASCADE,
        related_name='medicine',
        help_text='Model detail id'
    )

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)
