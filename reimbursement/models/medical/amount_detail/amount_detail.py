from django.db import models
from django.forms import forms

from erp_core.models import BaseModel

from reimbursement.models.medical import Medical


class AmountDetail(BaseModel):
    """
    This stores complete details of amount claimed, amount passed and amount rejected
    """
    # Claimed Amount
    amount_claimed_medicine = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='The amount claimed for the medicines, if any'
    )
    amount_claimed_test = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='The amount claimed for the tests, if any'
    )
    amount_claimed_room_rent = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='The amount claimed for room rented, if any'
    )
    amount_claimed_other = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='Others, Ex :- Operation, Procedure, ICU / CCU/ Consultation / Others)'
    )
    other_expenses = models.CharField(
        null=True,
        blank=True,
        max_length=150,
        help_text='Please specify, Ex :- Operation, Procedure, ICU / CCU/ Consultation / Others)'
    )
    # Passed Amount
    amount_passed_medicine = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='The amount passed for the medicines, if any'
    )
    amount_passed_test = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='The amount passed for the tests, if any'
    )
    amount_passed_room_rent = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='The amount passed for room rented, if any'
    )
    amount_passed_other = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='Others, Ex :- Operation, Procedure, ICU / CCU/ Consultation / Others)'
    )
    # Total Amount Claimed
    total_amount_claimed = models.DecimalField(
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='Total amount claimed'
    )
    total_amount_passed = models.DecimalField(
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='Total amount passed'
    )
    total_amount_rejected = models.DecimalField(
        blank=True,
        max_digits=12,
        decimal_places=2,
        help_text='Total amount rejected'
    )
    medical_reimbursement_register_page_no = models.PositiveIntegerField(
        help_text='Medical reimbursement register page number'
    )
    medical_reimbursement_register_sr_no = models.PositiveIntegerField(
        unique=True,
        help_text='Medical reimbursement register serial number'
    )
    # One to One relationship with Main Model i.e Medical
    medical = models.OneToOneField(
        Medical,
        related_name='amount_detail',
        help_text='Refers to Medical Model'
    )

    def clean(self):
        """
        This method overrides the default clean method of BaseModel.Model.
        This function add extra functionality that checks
         > if at least one claim amount is mentioned
        :return:
        """
        if not self.amount_claimed_medicine \
                and not self.amount_claimed_test \
                and not self.amount_claimed_room_rent \
                and not self.amount_claimed_other:
            raise forms.ValidationError('Please fill at least one claim amount')

    def save(self, *args, **kwargs):
        """
        This method overrides the default save method of BaseModel.Model.
        This function calculates total_amount_claimed, total_amount_passed and total_amount_rejected values and adds it
        to the respective fields
        :param args:
        :param kwargs:
        :return:
        """
        # For Claimed Amount
        self.total_amount_claimed = 0
        if self.amount_claimed_medicine:
            self.total_amount_claimed += self.amount_claimed_medicine
        if self.amount_claimed_test:
            self.total_amount_claimed += self.amount_claimed_test
        if self.amount_claimed_room_rent:
            self.total_amount_claimed += self.amount_claimed_room_rent
        if self.amount_claimed_other:
            self.total_amount_claimed += self.amount_claimed_other

        # For Passed Amount
        self.total_amount_passed = 0
        if self.amount_passed_medicine:
            self.total_amount_passed += self.amount_passed_medicine
        if self.amount_passed_test:
            self.total_amount_passed += self.amount_passed_test
        if self.amount_passed_room_rent:
            self.total_amount_passed += self.amount_passed_room_rent
        if self.amount_passed_other:
            self.total_amount_passed += self.amount_passed_other

        # For Rejected Amount
        self.total_amount_rejected = self.total_amount_claimed - self.total_amount_passed

        super(AmountDetail, self).save(*args, **kwargs)
