from django.db import models

from django.contrib.auth.models import User, Group

from django_fsm import FSMField

from erp import settings

from erp_core.models import BaseModel

from .professional_tour import ProfessionalTour
from .state import STATE


class ProfessionalTourTransitionHistory(BaseModel):
    """
    Stores transition that took place on a professional tour reimbursement model
    """
    class Meta:
        ordering = ['-created_at']

    professional = models.ForeignKey(
        ProfessionalTour,
        on_delete=models.CASCADE,
        help_text='Professional Tour',
        related_name='professional_tour_transition_history'
    )
    state_from = FSMField(
        null=True,
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
        related_name='professional_tour_transition_history'
    )
    remarks = models.CharField(
        null=True,
        blank=True,
        max_length=300,
        help_text='Remarks'
    )