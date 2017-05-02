# This file is not being used
# Just for future purpose

# from django.db import models
#
# from erp import settings
#
# from erp_core.models import BaseModel
#
# from reimbursement.models.medical import Medical
#
# from django_fsm import FSMField
#
# from state import STATE
#
#
# class Transition(BaseModel):
#     """
#     Stores transition that is allowed to take place in a medical reimbursement workflow
#     """
#     state_from = FSMField(
#         blank=True,
#         protected=not settings.DEBUG,
#         default=STATE.SUBMITTED,
#     )
#     state_to = FSMField(
#         blank=True,
#         protected=not settings.DEBUG,
#         default=STATE.SUBMITTED,
#     )
#     medical = models.ManyToManyField(
#         Medical,
#         through='TransitionHistory',
#         related_name='TMTM'
#     )
#
#     def __str__(self):
#         return str(self.state_from) + " - " + str(self.state_to)
#
#     def __unicode__(self):
#         return str(self.state_from) + " - " + str(self.state_to)