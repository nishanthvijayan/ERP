from django.shortcuts import render, get_object_or_404
from django.http import Http404

from reimbursement.models.medical import Medical


def generate_state_change_dealing_assistant(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    context = {
        "medical" : medical
    }
    return render(request, 'reimbursement/medical/state_change/role_based/dealing_assistant.html', context)
