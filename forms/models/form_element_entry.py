from django.db import models
from workflow_entry import WorkflowEntry
from form_element import FormElement

class FormElementEntry(models.Model):
    workflow_entry = models.ForeignKey(WorkflowEntry, on_delete=models.CASCADE)
    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
