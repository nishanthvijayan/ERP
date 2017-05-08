from django.db import models

from erp_core.models import BaseModel

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense


def generate_filename(instance, filename):
    """
    This generates proper path and file names for the images
    :type instance: object
    :type filename: str
    """
    return 'reimbursement/user_{0}/telephone_expense/bills/{1}'.\
        format(instance.telephone_expense.employee.user.id, filename)


class BillImage(BaseModel):
    """
    This stores images of the bills of the telephone expenses to be reimbursed
    """
    image_file = models.ImageField(
        upload_to=generate_filename,
        help_text='Upload Image of bills'
    )
    telephone_expense = models.ForeignKey(
        TelephoneExpense,
        related_name='bill_image_set'
    )

    def __str__(self):
        return 'Form#' + str(self.telephone_expense_id) + ' - ' + str(self.id)

    def __unicode__(self):
        return 'Form#' + str(self.telephone_expense_id) + ' - ' + str(self.id)
