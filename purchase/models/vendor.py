"""Model representing Vendor detaills in a purchase indent request."""

from django.db import models

from erp_core.models import BaseModel
from purchase.models import PurchaseIndentRequest


class Vendor(BaseModel):
    """This stores all the information regarding a vendor."""

    purchase_request = models.ForeignKey(PurchaseIndentRequest, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.EmailField(max_length=500)
    email = models.TextField(max_length=50)

    def __str__(self):
        """Return string representing the vendor by its Name."""
        return str(self.name)

    def __unicode__(self):
        """Return string representing the vendor by its Name."""
        return str(self.name)
