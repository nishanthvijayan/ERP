from django.db import models

from django.contrib.auth.models import User

from django_fsm import FSMField

from erp import settings

from erp_core.models import BaseModel

from .telephone_expense import TelephoneExpense
from .state import STATE


class TelephoneExpenseTransitionHistory(BaseModel):
    """
    Stores transition that took place on a medical reimbursement model
    """
    telephone_expense = models.ForeignKey(
        TelephoneExpense,
        on_delete=models.CASCADE,
        help_text='Telephone Expense',
        related_name='transition_history_set'
    )
    state_from = FSMField(
        null=True,
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )
    state_to = FSMField(
        null=True,
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )
    approved_by = models.ForeignKey(
        User,
        help_text='Employee',
        related_name='transition_history_set'
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        help_text='Remarks'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "#" + str(self.telephone_expense_id) \
               + " - " + str(self.state_from) \
               + " - " + str(self.state_to)

    def __unicode__(self):
        return "#" + str(self.telephone_expense_id) \
               + " - " + str(self.state_from) \
               + " - " + str(self.state_to)