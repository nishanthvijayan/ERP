from django.db import models

from erp_core.models.base_model import BaseModel

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour


class MeetingDate(BaseModel):
    """
    This stores all the information regarding professional tour reimbursement of an employee 
    """
    meeting_date = models.DateField(
        help_text='Mention dates of meeting or conference'
    )
    professional_tour = models.ForeignKey(
        ProfessionalTour,
        on_delete=models.CASCADE,
        help_text=''
    )

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)