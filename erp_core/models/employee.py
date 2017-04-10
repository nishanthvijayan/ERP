from django.contrib.auth.models import User
from django.db import models

from department import Department
from address import Address
from pay import Pay
from base_model import BaseModel


class Employee(BaseModel):
    employee_id = models.IntegerField(
        null=False,
        blank=False,
        help_text='UID for each employee'
    )
    nationality = models.CharField(
        null=False,
        blank=False,
        max_length=50
    )
    date_of_joining = models.DateField(
        null=False,
        blank=False,
    )
    designation = models.CharField(
        null=False,
        blank=False,
        max_length=100
    )
    short_designation = models.CharField(
        null=False,
        blank=False,
        max_length=100
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    current_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='current_address'
    )
    permanent_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='permanent_address'
    )
    pay = models.ForeignKey(
        Pay,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __unicode__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)
