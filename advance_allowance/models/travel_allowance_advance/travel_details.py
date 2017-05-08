from django.db import models

from erp_core.models import BaseModel
from advance_allowance.models.travel_allowance_advance.travel_allowance_advance import TravelAllowanceAdvance
from erp_core.models.employee import Employee


class TravelDetails(BaseModel):
    """
    This stores all the information regarding tour program back and forth.
    """
    travel_allowance_advance = models.ForeignKey(
        TravelAllowanceAdvance,
        help_text='Travel Detail'
    )
    date = models.DateField(
        help_text='Mention the date of journey'
    )
    from_place = models.CharField(
        max_length=100,
        help_text='Place from where flight/train/bus started'
    )
    to_place = models.CharField(
        max_length=100,
        help_text='Place where flight/train/bus stopped'
    )
    travel_mode =  models.CharField(
        max_length=100,
        help_text='Mention the mode of travel'
    )