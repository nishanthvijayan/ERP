from django.db import models
from workflow import Workflow

from positions.fields import PositionField


class FormElement(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    hint = models.CharField(max_length=500, blank=True)
    AVAILABLE_ELEMENT_TYPES = (
        ('text_input', 'Text Input'),
        ('number_input', 'Number Input'),
        ('date_input', 'Date Input'),
        ('time_input', 'Time Input'),
        ('date_time_input', 'Date Time Input'),
        ('text_area', 'Text Area')
    )
    element_type = models.CharField(max_length=50, choices=AVAILABLE_ELEMENT_TYPES)
    position = PositionField(collection='workflow')

    class Meta(object):
        ordering = ['position']

    def __str__(self):
        return self.caption
