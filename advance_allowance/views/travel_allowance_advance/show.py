from django.shortcuts import render
from django.http import Http404

from advance_allowance.models.travel_allowance_advance.travel_allowance_advance import TravelAllowanceAdvance
from advance_allowance.models.travel_allowance_advance.travel_details import TravelDetails


def show(request, travel_allowance_advance_id):
    travel_allowance_advance = TravelAllowanceAdvance.objects.filter(id=travel_allowance_advance_id).first()
    travel_details = TravelDetails.objects.filter(travel_allowance_advance_id=travel_allowance_advance_id)
    # print travel_details
    context = {
        'travel_allowance_advance': travel_allowance_advance,
        'travel_details': travel_details
    }
    return render(request, 'advance_allowance/travel_allowance_advance/show.html', context)