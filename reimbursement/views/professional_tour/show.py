from django.shortcuts import render
from django.http import Http404

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour

from reimbursement.models.professional_tour.meeting_date.meeting_date import MeetingDate


def show(request, professional_tour_id):
    professional_tour = ProfessionalTour.objects.filter(id=professional_tour_id).first()
    meeting_dates = MeetingDate.objects.filter(professional_tour_id=professional_tour_id)
    print meeting_dates
    context = {
        'professional_tour' : professional_tour,
        'meeting_dates' : meeting_dates,
    }
    return render(request,'reimbursement/professional_tour/show.html',context)


