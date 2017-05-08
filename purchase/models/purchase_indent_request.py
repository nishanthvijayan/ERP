"""Model representing Purchase Indent request."""

from django.db import models
from erp import settings

from django_fsm import FSMField, transition

from erp_core.models import BaseModel, Employee

from state import STATE


class PurchaseIndentRequest(BaseModel):
    """This stores all the information regarding a purchase indent of an employee."""

    indenter = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    budget_head = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    make_or_model_reason = models.TextField(max_length=500, null=True, blank=True)
    proprietary_owner = models.CharField(max_length=100, null=True, blank=True)
    proprietary_distributor = models.CharField(max_length=100, null=True, blank=True)

    state = FSMField(
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED
    )

    budgetary_approval = models.ImageField(upload_to='budgetary_approval', blank=True)
    directors_approval = models.ImageField(upload_to='directors_approval', blank=True)
    project_approval = models.ImageField(upload_to='project_approval', blank=True)

    budget_sanctioned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_already_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_available = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # expenditure dubitable_to field

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.APPROVED_BY_HOD)
    def hod_approve(self):
        """HOD approves the indent form."""
        print "HOD approved this form. Current state:", self.state

    @transition(field=state, source=STATE.APPROVED_BY_HOD, target=STATE.APPROVED_BY_JAO)
    def jao_approve(self):
        """JAO approves the indent form."""
        print "JAO approved this form. Current state:", self.state

    @transition(field=state, source=STATE.APPROVED_BY_JAO, target=STATE.APPROVED_BY_DR)
    def dr_approve(self):
        """DR approves the indent form."""
        print "DR approved this form. Current state:", self.state

    @transition(field=state, source=[STATE.SUBMITTED, STATE.APPROVED_BY_HOD, STATE.APPROVED_BY_JAO],
                target=STATE.REJECT)
    def reject(self):
        """Reject the indent form."""
        print "This form has been rejected. Current state:", self.state

    def __str__(self):
        """Return string representing the form as Name of Indentor[space]Created time."""
        return str(self.indenter.user.first_name) + ' ' \
            + str(self.indenter.user.last_name) + ' ' \
            + str(self.created_at)

    def __unicode__(self):
        """Return string representing the form as Name of Indentor[space]Created time."""
        return str(self.indenter.user.first_name) + ' ' \
            + str(self.indenter.user.last_name) + ' ' \
            + str(self.created_at)
