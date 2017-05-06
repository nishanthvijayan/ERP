from django.db import models

from django.contrib.auth.models import User, Group

from django_fsm import FSMField

from erp import settings

from erp_core.models import BaseModel

from .mp_hall import MpHall
from .state import STATE


class TransitionHistory(BaseModel):
    """
    Stores transition that took place on a medical reimbursement model
    """
    mp_hall = models.ForeignKey(
        MpHall,
        on_delete=models.CASCADE,
        help_text='MpHall',
        related_name='mp_hall_transition_history'
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
        related_name='mp_hall_transition_history'
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
        return "#" + str(self.mp_hall_id) \
               + " - " + str(self.state_from) \
               + " - " + str(self.state_to)

    def __unicode__(self):
        return "#" + str(self.mp_hall_id) \
               + " - " + str(self.state_from) \
               + " - " + str(self.state_to)