from django.db import models
from django.contrib.auth.models import User, Group
from django_fsm import FSMField

from erp import settings
from erp_core.models import BaseModel

from .travel_allowance_advance import TravelAllowanceAdvance
from .state import STATE


class TransitionHistory(BaseModel):
    """
    Stores transition that took place on a medical reimbursement model
    """
    travel_allowance_advance = models.ForeignKey(
        TravelAllowanceAdvance,
        on_delete=models.CASCADE,
        help_text='TA and Advance Form',
        related_name='ta_advance_form_transition_history'
    )
    state_from = FSMField(
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )
    state_to = FSMField(
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )
    approved_by = models.ForeignKey(
        User,
        help_text='Employee',
        related_name='ta_advance_form_transition_history'
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        help_text='Remarks'
    )

    class Meta:
        ordering = ['-created_at']
