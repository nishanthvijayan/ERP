from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django_fsm import can_proceed

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE
from reimbursement.models.medical.transition_history import TransitionHistory


def generate_state_change_junior_accounting_officer(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    remarks_error = ""
    if request.method == 'POST':
        if request.POST.get('AMOUNT_TRANSFERRED', False):
            if not can_proceed(medical.approve_by_jr_ao):
                raise PermissionDenied
            transition = TransitionHistory.objects.create(
                state_from=STATE.APPROVED_BY_R,
                state_to=STATE.AMOUNT_TRANSFERRED,
                remarks=request.POST.get('state-change-remarks', ''),
                approved_by=request.user,
                medical=medical
            )
            transition.save()
            medical.approve_by_jr_ao()
            medical.save()
            messages.success(request, 'Request for medical reimbursement #'
                             + str(medical_id)
                             + ' successfully approved!')
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
    return render(request, 'reimbursement/medical/state_change/role_based/junior_accounting_officer.html', context)
