from django.db import models
from erp import settings

from django_fsm import FSMField, transition

from erp_core.models import BaseModel

from general_detail import GeneralDetail

from state import STATE


class Medical(BaseModel):
    """
    This stores all the information regarding medical reimbursement of an employee
    """
    general_detail = models.ForeignKey(
        GeneralDetail,
        help_text='General Detail'
    )
    state = FSMField(
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )

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

    @transition(field=state, source=STATE.APPROVED_BY_DA, target=STATE.APPROVED_BY_MS)
    def approve_by_ms(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_MS, target=STATE.APPROVED_BY_DR)
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

    @transition(field=state, source=STATE.APPROVED_BY_DA, target=STATE.REJECTED_BY_MS)
    def reject_by_ms(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_MS, target=STATE.REJECTED_BY_DR)
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
        return str(self.general_detail.employee.user.first_name) + ' ' \
               + str(self.general_detail.employee.user.last_name) \
               + " - " + str(self.id)

    def __unicode__(self):
        return str(self.general_detail.employee.user.first_name) + ' ' \
               + str(self.general_detail.employee.user.last_name) \
               + " - " + str(self.id)
