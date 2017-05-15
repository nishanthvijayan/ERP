from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from django_fsm import can_proceed

from reimbursement.models.professional_tour.professional_tour import ProfessionalTour
from reimbursement.models.professional_tour.state import STATE
from reimbursement.models.professional_tour.professional_tour_transition_history import ProfessionalTourTransitionHistory


def generate_state_change_assistant_registrar(request, professional_tour_id):
    professional_tour = get_object_or_404(ProfessionalTour, id=professional_tour_id)
    remarks_error = ""
    if request.metar == 'POST':
        if request.POST.get('APPROVED_BY_AR', False):
            if not can_proceed(professional_tour.approve_by_ar):
                raise PermissionDenied
            transition = ProfessionalTourTransitionHistory.objects.create(
                state_from=STATE.APPROVED_BY_SrAO,
                state_to=STATE.APPROVED_BY_AR,
                remarks=request.POST.get('state-change-remarks', ''),
                approved_by=request.user,
                professional_tour=professional_tour
            )
            transition.save()
            professional_tour.approve_by_ar()
            professional_tour.save()
            messages.success(request, 'Request for Professional Tour Reimbursement #'
                             + str(professional_tour_id)
                             + ' successfully approved!')
            return redirect('reimbursement:professional-tour-show', professional_tour_id)
        elif request.POST.get('REJECTED_BY_AR', False):
            if not can_proceed(professional_tour.reject_by_ar):
                raise PermissionDenied
            transition = ProfessionalTourTransitionHistory.objects.create(
                state_from=STATE.SUBMITTED,
                state_to=STATE.REJECTED_BY_AR,
                remarks=request.POST.get('state-change-remarks', ''),
                approve_by=request.user,
                professional_tour=professional_tour
            )
            transition.save()
            professional_tour.reject_by_ar()
            professional_tour.save()
            messages.success(request, 'Request for Professional Tour Reimbursement #' + str(professional_tour_id)
                             + ' successfully rejected!')
            return redirect('reimbursement:professional-tour-show', professional_tour_id)
        else:
            raise PermissionDenied

    context = {
        "professional_tour": professional_tour,
        "form": {
            "remarks": {
                "errors": remarks_error
            }
        }
    }
    return render(request, 'reimbursement/professional_tour/state_change/role_based/assistant_registrar.html', context)