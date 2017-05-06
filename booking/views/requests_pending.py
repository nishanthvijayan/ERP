from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from erp_core.models import Employee

from booking.models.mp_hall.mp_hall import MpHall
from booking.models.mp_hall.state import STATE


def booking_requests_pending(request):
    if request.user.groups.filter(name='Booking_MPHall_Change_State').exists():
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
    employee = request.user.employee_set.all().first()
    if employee:
        if employee.department.hod.user.id == employee.user.id:
            mp_hall_list = MpHall.objects.filter(state=STATE.SUBMITTED)
        elif request.user.groups.filter(name='HindiTranslator').exists():
            mp_hall_list = MpHall.objects.filter(state=STATE.APPROVED_BY_HOD)
        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists():
            mp_hall_list = MpHall.objects.filter(state=STATE.APPROVED_BY_DA)
        else:
            mp_hall_list = MpHall.objects.none()
        return mp_hall_list




