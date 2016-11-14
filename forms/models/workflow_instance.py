from django.db import models
from django.contrib.auth.models import User
from workflow import Workflow
from state import State

class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    current_state = models.ForeignKey(State, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
