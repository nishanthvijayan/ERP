from django.db import models

from django_fsm import transition, FSMField

from erp import settings

from erp_core.models import BaseModel, Employee

from state import STATE


class TelephoneExpense(BaseModel):
    """
    This stores details of the telephone expenses to be reimbursed
    """
    employee = models.ForeignKey(
        Employee,
        related_name='telephone_expenses'
    )
    register_page_no = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Enter page number of the register'
    )
    register_serial_no = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Enter serial number for the record in the register'
    )
    amount_passed = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the amount passed for reimbursement'
    )
    state = FSMField(
        null=True,
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )

    class Meta:
        verbose_name = "Telephone Expense"

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.APPROVED_BY_DA)
    def approve_by_da(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_DA, target=STATE.APPROVED_BY_DR)
    def approve_by_dr(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_DR, target=STATE.APPROVED_BY_SrAO)
    def approve_by_sr_ao(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_SrAO, target=STATE.APPROVED_BY_R)
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

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.REJECTED_BY_DA)
    def reject_by_da(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_DA, target=STATE.REJECTED_BY_DR)
    def reject_by_dr(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_DR, target=STATE.REJECTED_BY_SrAO)
    def reject_by_sr_ao(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_SrAO, target=STATE.REJECTED_BY_R)
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
        return str(self.id) + ' - ' + str(self.employee.user.first_name) + ' - ' + str(self.employee.user.last_name)

    def __unicode__(self):
        return str(self.id) + ' - ' + str(self.employee.user.first_name) + ' - ' + str(self.employee.user.last_name)