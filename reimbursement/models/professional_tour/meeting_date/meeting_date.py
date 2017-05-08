from django.db import models

from erp_core.models.base_model import BaseModel

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour


class MeetingDate(BaseModel):
    """
    This stores all the information regarding professional tour reimbursement of an employee 
    """
    meeting_date = models.DateField(
        help_text='Mansion dates of meeting or conference'
    )
    professional = models.ForeignKey(
        ProfessionalTour,
        on_delete=models.CASCADE,
        help_text=''
    )