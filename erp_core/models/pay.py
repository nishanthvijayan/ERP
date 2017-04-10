from django.db import models

from base_model import BaseModel


class Pay(BaseModel):
    """
    This stores structured detailed annual payment/salary of an employee working for the institute
    """
    band = models.IntegerField(
        null=False,
        blank=False,
        help_text='Band Pay'
    )
    grade = models.IntegerField(
        null=False,
        blank=False,
        help_text='Grade Pay'
    )
    da = models.IntegerField(
        null=False,
        blank=False,
        help_text='Dearness Allowance'
    )
    hra = models.IntegerField(
        null=False,
        blank=False,
        help_text='House Rental Allowance'
    )
    ta = models.IntegerField(
        null=False,
        blank=False,
        help_text='Travel Allowance'
    )
    gross = models.IntegerField(
        null=False,
        blank=True,
        help_text='Gross Total = Band + Grade + DA + HRA + TA'
    )
    nps = models.IntegerField(
        null=False,
        blank=False,
        help_text='New Pension Scheme'
    )
    lic = models.IntegerField(
        null=False,
        blank=False,
        help_text='LIC'
    )
    deduction = models.IntegerField(
        null=False,
        blank=True,
        help_text='Deductions = NPS + LIC'
    )
    net_salary = models.IntegerField(
        null=False,
        blank=True,
        help_text='Net Salary = Gross Total - Deductions'
    )

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        This method overrides the default save method of BaseModel.Model.
        This function calculates gross, deduction and net_salary values and adds it to the respective fields
        :param args:
        :param kwargs:
        :return:
        """
        self.gross = self.band + self.grade + self.da + self.hra + self.ta
        self.deduction = self.nps + self.lic
        self.net_salary = self.gross - self.deduction
        super(Pay, self).save(*args, **kwargs)
