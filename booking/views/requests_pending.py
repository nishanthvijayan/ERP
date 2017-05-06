from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from booking.models.mp_hall.mp_hall import MpHall
from booking.models.mp_hall.state import STATE


def booking_requests_pending(request):
    if request.user.groups.filter(name='MP_Hall_Change_State').exists():
        mp_hall_list = get_mp_hall_list(request)
        page = request.GET.get('page')
        paginator = Paginator(mp_hall_list, 10)
        try:
            mp_halls = paginator.page(page)
        except PageNotAnInteger:
            mp_halls = paginator.page(1)
        except EmptyPage:
            mp_halls = paginator.page(paginator.num_pages)
        context = {
            'mp_halls': mp_halls
        }
        return render(request, 'booking/requests_pending.html', context)
    else:
        raise Http404


def get_mp_hall_list(request):
    if request.user.id ==
