from django.db import models
from django.contrib.auth.models import User
from workflow import Workflow
from state import State


class WorkflowEntry(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    current_state = models.ForeignKey(State, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.workflow.name + ' submitted by ' + self.creator.username
