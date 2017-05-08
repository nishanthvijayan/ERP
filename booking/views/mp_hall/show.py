from django.shortcuts import render
from django.http import Http404

from booking.models.mp_hall.mp_hall import MpHall


def show(request, mp_hall_id):
    mp_hall = MpHall.objects.filter(id=mp_hall_id).first()
    context = {
        'mp_hall' : mp_hall
    }
    print mp_hall
    return render(request,'booking/mp_hall/show.html',context)
