from django.db import models

from erp_core.models import BaseModel

from general_detail import GeneralDetail


class Medical(BaseModel):
    """
    This stores all the information regarding medical reimbursement of an employee
    """
    general_detail = models.ForeignKey(
        GeneralDetail,
        help_text='General details ID of the GeneralDetail'
    )

    def __str__(self):
        return str(self.general_detail.employee.user.first_name) + ' ' \
               + str(self.general_detail.employee.user.last_name)

    def __unicode__(self):
        return str(self.general_detail.employee.user.first_name) + ' ' \
               + str(self.general_detail.employee.user.last_name)
