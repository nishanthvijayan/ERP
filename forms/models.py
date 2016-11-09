from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class FormElementType(models.Model):
    kind = models.CharField(max_length=200)
    
    def __str__(self):
        return self.kind

class FormElement(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    element_type = models.ForeignKey(FormElementType, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200)
    hint = models.CharField(max_length=500)

    def __str__(self):
        return self.caption

class FormElementListItem(models.Model):
    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class State(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Transition(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    from_state = models.ForeignKey(State, on_delete=models.CASCADE)
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.from_state + ' -> ' + self.to_state

class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    current_state = models.ForeignKey(State, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class FormElementInstance(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    form_element = models.ForeignKey(FormElement, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)

