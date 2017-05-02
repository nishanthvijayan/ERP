from django.db import models
from erp import settings

from django_fsm import FSMField

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

    def __str__(self):
        return str(self.general_detail.employee.user.first_name) + ' ' \
               + str(self.general_detail.employee.user.last_name) \
               + " - " + str(self.id)

    def __unicode__(self):
        return str(self.general_detail.employee.user.first_name) + ' ' \
               + str(self.general_detail.employee.user.last_name) \
               + " - " + str(self.id)
