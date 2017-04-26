"""Model representing Item detaills in a purchase indent request."""

from django.db import models

from erp_core.models import BaseModel
from purchase.models import PurchaseIndentRequest


class Item(BaseModel):
    """This stores all the information regarding an Item."""

    purchase_request = models.ForeignKey(PurchaseIndentRequest, on_delete=models.CASCADE)
    specification = models.TextField(max_length=500)
    quantity = models.IntegerField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """Return string representing the Item by its Specification."""
        return str(self.specification)

    def __unicode__(self):
        """Return string representing the Item by its Specification."""
        return str(self.specification)
