from django.db import models
from django.contrib.auth.models import Group


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    allowed_groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

    def initial_state(self):
        try:
            return self.state_set.filter(kind='Initial')[0]
        except IndexError:
            return None
