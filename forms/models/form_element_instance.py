from django.db import models
from workflow import Workflow
from form_element import FormElement

class FormElementInstance(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
