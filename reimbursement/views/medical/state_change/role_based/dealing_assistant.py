from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django_fsm import can_proceed

from reimbursement.models.medical import Medical
from reimbursement.models.medical.state import STATE
from reimbursement.models.medical.transition_history import TransitionHistory

from reimbursement.forms.medical.amount_detail.amount_detail import AmountDetailForm


def generate_state_change_dealing_assistant(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    if request.method == 'POST':
        form = AmountDetailForm(data=request.POST, instance=medical.amount_detail)
        if form.is_valid():
            if request.POST.get('VERIFIED_BY_DA', False):
                if form.save():
                    if not can_proceed(medical.verify_by_da):
                        raise PermissionDenied
                    transition = TransitionHistory.objects.create(
                        state_from=STATE.SUBMITTED,
                        state_to=STATE.VERIFIED_BY_DA,
                        remarks=request.POST.get('state-change-remarks', ''),
                        approved_by=request.user,
                        medical=medical
                    )
                    transition.save()
                    medical.verify_by_da()
                    medical.save()
                    messages.success(request, 'Request for medical reimbursement #' + str(medical_id)
                                     + ' successfully approved!')
                    return redirect('reimbursement:medical-show', medical_id)
                else:
                    messages.error(request, 'Please resolve the errors below and try again')
            if request.POST.get('REJECTED_BY_DA', False):
                if not can_proceed(medical.reject_by_da):
                    raise PermissionDenied
                transition = TransitionHistory.objects.create(
                    state_from=STATE.SUBMITTED,
                    state_to=STATE.REJECTED_BY_DA,
                    remarks=request.POST.get('state-change-remarks', ''),
                    approved_by=request.user,
                    medical=medical
                )
                transition.save()
                medical.reject_by_da()
                medical.save()
                messages.success(request, 'Request for medical reimbursement #' + str(medical_id)
                                 + ' successfully rejected!')
    else:
        form = AmountDetailForm()
    context = {
        "medical": medical,
        "form": form
    }
    return render(request, 'reimbursement/medical/state_change/role_based/dealing_assistant.html', context)
