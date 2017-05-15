from django.db import models

from django_fsm import transition, FSMField

from erp_core.models.base_model import BaseModel

from erp import settings

from erp_core.models.employee import Employee

from state import STATE


class ProfessionalTour(BaseModel):
    """
    This stores all the information regarding professional tour reimbursement of an employee 
    """
    station_visited = models.CharField(
        max_length=100,
        help_text='Mention the station visited'
    )
    fair_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Enter the amount paid for fair for both ways'
    )
    expenditure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Enter the amount paid for boarding and lodging'
    )
    purpose_visit = models.CharField(
        max_length=100,
        help_text='Mention the purpose of visit'
    )
    approval = models.ImageField(
        null=True,
        blank=True,
        help_text='attach image of approval of director or HOD if obtained?'
    )
    information = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Any other information'
    )
    amount_spent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Enter the amount spent on local journey'
    )
    advance_taken = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Enter the advance amount taken'
    )
    reimbursement_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Enter the amount of reimbursement'
    )
    amount_passed = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        help_text='Enter amount that passed '
    )
    cheque_no = models.PositiveIntegerField(
        null=True,
        help_text='Enter cheque no.'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )
    state = FSMField(
        null=True,
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )

    class Meta:
        verbose_name = "Professional Tour"

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

    @transition(field=state, source=STATE.APPROVED_BY_HOD, target=STATE.VERIFIED_BY_DA)
    def verified_by_da(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.VERIFIED_BY_DA, target=STATE.APPROVED_BY_SrAO)
    def verified_by_sr_ao(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_SrAO  , target=STATE.APPROVED_BY_AR)
    def approve_by_ar(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_AR, target=STATE.APPROVED_BY_R)
    def approve_by_r(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_R, target=STATE.AMOUNT_TRANSFERRED)
    def approve_by_jr_ao(self):
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

    @transition(field=state, source=STATE.VERIFIED_BY_DA, target=STATE.REJECTED_BY_SrAO)
    def reject_by_sr_ao(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_SrAO, target=STATE.REJECTED_BY_AR)
    def reject_by_ar(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_AR, target=STATE.REJECTED_BY_R)
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
        return  str(self.id)



