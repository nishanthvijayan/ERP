from django.db import models

from erp_core.models import BaseModel

from medical_detail import MedicalDetail


def generate_filename(instance, filename):
    """
    This generates proper path and file names for the images
    :type instance: object
    :type filename: str
    """
    return 'reimbursement/user_{0}/medicine_bills/{1}'.\
        format(instance.medical_detail.medical.general_detail.employee.user.id, filename)


class MedicalBill(BaseModel):
    image_file = models.ImageField(
        upload_to=generate_filename,
        help_text='Upload Image of bills'
    )
    medical_detail = models.ForeignKey(
        MedicalDetail,
        on_delete=models.CASCADE,
        related_name='medicine_bill',
        help_text='Medical detail id'
    )
