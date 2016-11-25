from django.db import models


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def initial_state(self):
        try:
            return self.state_set.filter(kind='Initial')[0]
        except IndexError:
            return None
