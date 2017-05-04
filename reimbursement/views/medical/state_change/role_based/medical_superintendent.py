from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django_fsm import can_proceed

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE
from reimbursement.models.medical.transition_history import TransitionHistory


def generate_state_change_medical_superintendent(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    remarks_error = ""
    if request.method == 'POST':
        if request.POST.get('APPROVED_BY_MS', False):
            if not can_proceed(medical.approve_by_ms):
                raise PermissionDenied
            transition = TransitionHistory.objects.create(
                state_from=STATE.APPROVED_BY_DA,
                state_to=STATE.APPROVED_BY_MS,
                remarks=request.POST.get('state-change-remarks', ''),
                approved_by=request.user,
                medical=medical
            )
            transition.save()
            medical.approve_by_ms()
            medical.save()
            messages.success(request, 'Request for medical reimbursement #'
                             + str(medical_id)
                             + ' successfully approved!')
            return redirect('reimbursement:medical-show', medical_id)
        elif request.POST.get('REJECTED_BY_MS', False):
            if not can_proceed(medical.reject_by_ms):
                raise PermissionDenied
            transition = TransitionHistory.objects.create(
                state_from=STATE.APPROVED_BY_DA,
                state_to=STATE.REJECTED_BY_MS,
                remarks=request.POST.get('state-change-remarks', ''),
                approve_by=request.user,
                medical=medical
            )
            transition.save()
            medical.reject_by_ms()
            medical.save()
            messages.success(request, 'Request for medical reimbursement #' + str(medical_id)
                         + ' successfully rejected!')
            return redirect('reimbursement:medical-show', medical_id)
        else:
            raise PermissionDenied

    context = {
        "medical": medical,
        "form": {
            "remarks": {
                "errors": remarks_error
            }
        }
    }
    return render(request, 'reimbursement/medical/state_change/role_based/medical_superintendent.html', context)
