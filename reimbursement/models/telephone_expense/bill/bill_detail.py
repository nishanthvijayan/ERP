from django.db import models
from django.core.validators import RegexValidator

from erp_core.models import BaseModel

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense


class BillDetail(BaseModel):
    """
    This stores details of the bills of the telephone expenses to be reimbursed
    """
    telephone_expense = models.ForeignKey(
        TelephoneExpense,
        null=True,
        blank=True,
        help_text='Telephone Expense',
        related_name='bill_detail_set'
    )
    bill_number = models.CharField(
        max_length=10,
        help_text='Enter bill number mentioned on the bill'
    )
    bill_date = models.DateField(
        help_text='Enter date mentioned on the bill'
    )
    date_form = models.DateField(
        help_text='Enter starting date of the billing'
    )
    date_to = models.DateField(
        help_text='Enter finishing date of the billing'
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="Phone number must be entered in the format")
    phone_number = models.CharField(
        max_length=12,
        validators=[phone_regex],
        help_text='Enter phone number'
    )
    is_telephone_line = models.BooleanField(
        help_text='Is it a telephone number'
    )