from django.db import models


class BaseModel(models.Model):
    """
    This abstract model will provide base for all the models in the ERP System. This adds creation and modification timestamp to models.Model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
