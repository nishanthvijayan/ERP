from django.http import Http404
from django.shortcuts import render


from booking.models.mp_hall.mp_hall import MpHall

from booking.models.mp_hall.state import STATE

from booking.views.mp_hall.state_change.role_based.head_of_department import generate_state_change_head_of_department

from booking.views.mp_hall.state_change.role_based.dealing_assistant import generate_state_change_dealing_assistant

from booking.views.mp_hall.state_change.role_based.registrar import generate_state_change_registrar


def state_change(request, mp_hall_id):

    if MpHall.objects.filter(id=mp_hall_id).exists():
        employee = request.user.employee_set.all().first()
        if employee:
            if employee.department.hod.user.id == employee.user.id:
                if MpHall.objects.filter(id=mp_hall_id).filter(state=STATE.SUBMITTED).exists():
                    return generate_state_change_head_of_department(request, mp_hall_id)
                if request.user.groups.filter(name='HindiTranslator').exists() \
                        and MpHall.objects.filter(id=mp_hall_id).filter(state=STATE.APPROVED_BY_HOD).exists():
                    return generate_state_change_dealing_assistant(request, mp_hall_id)
                if request.user.groups.filter(name='R_AdministrativeDepartment').exists() \
                        and MpHall.objects.filter(id=mp_hall_id).filter(state=STATE.APPROVED_BY_DA).exists():
                    return generate_state_change_registrar(request, mp_hall_id)
                else:
                    raise Http404
    else:
        raise Http404