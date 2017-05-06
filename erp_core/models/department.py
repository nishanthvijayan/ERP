from django.db import models

from base_model import BaseModel


class Department(BaseModel):
    """
    This stores details about various departments in the Institute
    """
    name = models.CharField(
        null=False,
        blank=False,
        max_length=100
    )
    short_name = models.CharField(
        null=False,
        blank=False,
        max_length=20,
        help_text='Like CSE, EE, ME'
    )
    description = models.CharField(
        null=False,
        blank=False,
        max_length=500
    )
    hod = models.ForeignKey(
        'erp_core.Employee',
        null=True,
        blank=True,
        related_name='department_set',
        help_text='Head of the Department'
    )

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)
