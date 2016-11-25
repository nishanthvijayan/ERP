from django.db import models
from workflow import Workflow


class State(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    AVAILABLE_KINDS = (
        ('Initial', 'Initial'),
        ('Intermediate', 'Intermediate'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )
    kind = models.CharField(max_length=500, choices=AVAILABLE_KINDS)

    def __str__(self):
        return self.name
