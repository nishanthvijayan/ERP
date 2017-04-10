from django.db import models

from base_model import BaseModel


class Address(BaseModel):
    """
    This stores detailed addresses
    """
    address = models.CharField(
        max_length=150,
        null=False,
        blank=False
    )
    town_city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='This field is option as some places doesnt have town/city'
    )
    district = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    state = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    country = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    zipcode = models.IntegerField(
        null=False,
        blank=False
    )

    def __str__(self):
        return str(self.address) + ', ' +  str(self.town_city) + ', ' + str(self.district) + ', ' + str(self.state) + ', ' + str(self.country) + ', ' + str(self.zipcode)

    def __unicode__(self):
        return str(self.address) + ', ' + str(self.town_city) + ', ' + str(self.district) + ', ' + str(self.state) + ', ' + str(self.country) + ', ' + str(
            self.zipcode)
