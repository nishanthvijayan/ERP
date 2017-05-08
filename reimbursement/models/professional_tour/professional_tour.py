from django.db import models

from erp_core.models.base_model import BaseModel

from erp_core.models.employee import Employee


class ProfessionalTour(BaseModel):
    """
    This stores all the information regarding professional tour reimbursement of an employee 
    """
    station_visited = models.CharField(
        max_length=100,
        help_text='Mansion the station visited'
    )
    fair_paid = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Enter the amount paid for fair for both ways'
    )
    expenditure = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Enter the amount paid for boarding and lodging'
    )
    purpose_visit = models.CharField(
        max_length=100,
        help_text='Mansion the purpose of visit'
    )
    has_approval = models.BooleanField(
        help_text='Whether approval of director or HOD obtained?'
    )
    information = models.CharField(
        max_length=100,
        help_text='Any other information'
    )
    amount_spent = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Enter the amount spent on local journey'
    )
    advance_taken = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Enter the advance amount taken'
    )
    reimbursement_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text='Enter the amount of reimbursement'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )

