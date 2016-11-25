from django.db import models
from workflow import Workflow
from state import State


class Transition(models.Model):
    name = models.CharField(max_length=50)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    from_state = models.ForeignKey(State, on_delete=models.CASCADE)
    to_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.from_state.name + ' -> ' + self.to_state.name
