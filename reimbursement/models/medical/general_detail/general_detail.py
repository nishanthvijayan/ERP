from django.db import models

from erp_core.models import BaseModel, Employee


class GeneralDetail(BaseModel):
    """
    This stores general details in the reimbursement forms other than medical
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    patient_name = models.CharField(
        max_length=150,
        help_text='Full name of the patient'
    )
    patient_age = models.PositiveSmallIntegerField(
        help_text='Age of the patient'
    )
    employee_relationship = models.CharField(
        max_length=150,
        help_text='Relationship with the employee'
    )

    def __str__(self):
        return str(self.employee.user.first_name) + ' ' + str(self.employee.user.last_name)

    def __unicode__(self):
        return str(self.employee.user.first_name) + ' ' + str(self.employee.user.last_name)
