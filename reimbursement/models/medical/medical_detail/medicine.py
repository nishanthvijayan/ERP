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
        decimal_places=2
    )
    medical_detail = models.ForeignKey(
        MedicalDetail,
        on_delete=models.CASCADE,
        help_text='Model detail id'
    )
