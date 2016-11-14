from django.db import models
from django.contrib.auth.models import Group
from workflow import Workflow
from state import State

class Transition(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    from_state = models.ForeignKey(State, on_delete=models.CASCADE)
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='+')
    allowed_groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.from_state.name + ' -> ' + self.to_state.name
