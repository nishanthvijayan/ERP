from django.db import models
from django import forms

from django_fsm import transition, FSMField

from erp import settings

from erp_core.models import BaseModel, Employee

from state import STATE


class MpHall(BaseModel):
    """
        This stores the details of MP Hall Booking
    """
    date = models.DateField(
        help_text='Enter the date of booking'
    )
    from_time = models.TimeField(
        help_text='Enter the booking start time'
    )
    to_time = models.TimeField(
        help_text='Enter the booking end time'
    )
    purpose = models.CharField(
        max_length=100,
        help_text='Enter the purpose of booking'
    )
    laptop_req = models.IntegerField(
        help_text='Enter the number of laptops required'
    )
    projector_req = models.IntegerField(
        help_text='Enter the number of projectors required'
    )
    audio_req = models.IntegerField(
        help_text='Enter the number of audio systems required'
    )
    video_req = models.IntegerField(
        help_text='Enter the number of video conferencing systems required'
    )
    employee = models.ForeignKey(
        Employee,
        related_name='mp_hall_booking'
    )
    state = FSMField(
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.APPROVED_BY_HOD)
    def approve_by_hod(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_HOD, target=STATE.APPROVED_BY_DA)
    def approve_by_da(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_DA, target=STATE.APPROVED_BY_R)
    def approve_by_r(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.REJECTED_BY_HOD)
    def reject_by_hod(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_HOD, target=STATE.REJECTED_BY_DA)
    def reject_by_da(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_DA, target=STATE.REJECTED_BY_R)
    def reject_by_r(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)