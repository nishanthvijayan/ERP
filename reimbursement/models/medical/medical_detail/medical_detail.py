from django.db import models
from django.forms import forms
from django.core.validators import MinValueValidator

from decimal import Decimal

from erp_core.models import BaseModel

from reimbursement.models.medical import Medical


def diagnosis_advised_certificate_filename(instance, filename):
    return 'reimbursement/user_{0}/diagnosis_advised_certificate/{1}'.format(instance.id, filename)


class MedicalDetail(BaseModel):
    """
    This stores the form data filled in the hard copy of medical reimbursement form
    """
    # 6
    place_at_which_patient_fell_ill = models.CharField(
        max_length=150,
        help_text='Mention the place where the patient fell ill'
    )
    # 7(i)
    # --- Medical Attendance ---
    # Consultation by medical officer, ie a doctor
    # 7(i).a
    consultant_name = models.CharField(
        max_length=150,
        help_text='Full name of the medical officer'
    )
    # 7(i).(a).b
    consultant_designation = models.CharField(
        max_length=150,
        help_text='Designation of the medical officer'
    )
    consultant_hospital = models.CharField(
        max_length=200,
        help_text='Name of the hospital or dispensary'
    )
    # -----
    # 7(i).(b)
    consultation_place = models.CharField(
        max_length=150,
        help_text='Mention where consultation took place, for multiple places use commas'
    )
    # Consultation dates with fee in Consultation model
    injection_place = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        help_text='Mention the place where injection held, for multiple places use commas'
    )
    # Injection dates with fee in Injection model
    # -----
    # Charges for pathological, bacteriological, Radiological
    # or other similar tests under taken during diagnosis
    diagnosis_place = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        help_text='Mention the hospital or laboratory where diagnosis held'
    )
    # diagnosis_advised = models.BooleanField(
    #     help_text='Whether the tests were under taken on the advice of the authorized medical attendant. '
    #               'If so certificate to the effect should be attached.'
    # )
    diagnosis_advised_certificate = models.ImageField(
        null=True,
        blank=True,
        upload_to=diagnosis_advised_certificate_filename,
        help_text='Upload Image of the certificate'
    )
    # Cost of medicines purchased from market
    # Not required
    # cost_of_medicines_market = models.PositiveIntegerField(
    #     null=True,
    #     blank=True,
    #     help_text='Mention cost of medicines purchased from market'
    # )
    # 7(iii)
    # Upload cash memos/bills in image model

    # --- Consultation with specialist ---
    specialist_consultant_name = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        help_text='Full name of the Specialist'
    )
    specialist_consultant_designation = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        help_text='Designation of the Specialist'
    )
    specialist_consultant_hospital = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        help_text='Name of the hospital or dispensary'
    )
    # 7.(II).(a)
    # dates and fee in SpecialistConsultation model
    specialist_consultation_place = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        help_text='Mention where consultation with the specialist took place'
    )
    total_amount_claimed = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Mention total claim amount'
    )
    less_advance_taken = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Mention Less advance taken before'
    )
    net_amount_claimed = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Enter net amount, ie Total - Less Amount'
    )
    # List of Medicines
    # ----
    # One to One relationship with Main Model i.e Medical
    medical = models.OneToOneField(
        Medical,
        related_name='medical_detail',
        help_text='Refers to Medical Model'
    )

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def clean(self):
        """
        This method overrides the default clean method of BaseModel.Model.
        This function add extra functionality that checks
         > if diagnosis_advised is true than certificate image must be uploaded
        :return:
        """

        self.total_amount_claimed = self.net_amount_claimed
        if self.less_advance_taken:
            self.total_amount_claimed += self.less_advance_taken


        if not self.specialist_consultant_name \
                or not self.specialist_consultant_designation \
                or not self.specialist_consultant_hospital \
                or not self.specialist_consultation_place:
            if self.specialist_consultant_name \
                    or self.specialist_consultant_designation \
                    or self.specialist_consultant_hospital \
                    or self.specialist_consultation_place:
                raise forms.ValidationError('Please enter full details of specialist consultant')
            else:
                pass
        else:
            pass
