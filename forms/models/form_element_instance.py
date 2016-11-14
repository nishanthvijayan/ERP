from django.db import models
from workflow_instance import WorkflowInstance
from form_element import FormElement

class FormElementInstance(models.Model):
    workflow_instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE)
    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
