from django.db import models
from form_element import FormElement


class FormElementListItem(models.Model):

    '''
    Store a FormElementListItem.
    '''

    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name
