from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django_fsm import can_proceed

from booking.models.mp_hall.mp_hall import MpHall
from booking.models.mp_hall.state import STATE
from booking.models.mp_hall.transition_history import TransitionHistory


def generate_state_change_registrar(request, mp_hall_id):
    mp_hall = get_object_or_404(MpHall, id=mp_hall_id)
    remarks_error = ""
    if request.method == 'POST':
        if request.POST.get('APPROVED_BY_R', False):
            if not can_proceed(mp_hall.approve_by_r):
                raise PermissionDenied
            transition = TransitionHistory.objects.create(
                state_from=STATE.APPROVED_BY_DA,
                state_to=STATE.APPROVED_BY_R,
                remarks=request.POST.get('state-change-remarks', ''),
                approved_by=request.user,
                mp_hall=mp_hall
            )
            transition.save()
            mp_hall.approve_by_r()
            mp_hall.save()
            messages.success(request, 'Request for MP Hall Booking #'
                             + str(mp_hall_id)
                             + ' successfully approved!')
            return redirect('booking:mp-hall-show', mp_hall_id)
        elif request.POST.get('REJECTED_BY_R', False):
            if not can_proceed(mp_hall.reject_by_r):
                raise PermissionDenied
            transition = TransitionHistory.objects.create(
                state_from=STATE.APPROVED_BY_DA,
                state_to=STATE.REJECTED_BY_R,
                remarks=request.POST.get('state-change-remarks', ''),
                approve_by=request.user,
                mp_hall=mp_hall
            )
            transition.save()
            mp_hall.reject_by_r()
            mp_hall.save()
            messages.success(request, 'Request for MP Hall Booking #' + str(mp_hall_id)
                             + ' successfully rejected!')
            return redirect('booking:mp-hall-show', mp_hall_id)
        else:
            raise PermissionDenied

    context = {
        "mp_hall": mp_hall,
        "form": {
            "remarks": {
                "errors": remarks_error
            }
        }
    }
    return render(request, 'booking/mp_hall/state_change/role_based/registrar.html', context)
