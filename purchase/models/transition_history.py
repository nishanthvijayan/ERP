"""Model representing Purchase Indent request."""

from django.db import models
from erp_core.models import BaseModel, Employee
from purchase.models import PurchaseIndentRequest


class TransitionHistory(BaseModel):
    """This stores all the information regarding a purchase indent of an employee."""

    approver = models.ForeignKey(Employee, on_delete=models.CASCADE)
    form = models.ForeignKey(PurchaseIndentRequest, on_delete=models.CASCADE)

    from_state = models.CharField(max_length=50)
    to_state = models.CharField(max_length=50)
    remark = models.TextField(max_length=500)

    def __str__(self):
        """Return string representing transition history."""
        return str(self.approver.user.first_name) + ' ' \
            + str(self.approver.user.last_name) + ' ' \
            + str(self.created_at) + ' ' \
            + str(self.from_state) + '->' + str(self.to_state)

    def __unicode__(self):
        """Return string representing transition history."""
        return str(self.approver.user.first_name) + ' ' \
            + str(self.approver.user.last_name) + ' ' \
            + str(self.created_at) + ' ' \
            + str(self.from_state) + '->' + str(self.to_state)
