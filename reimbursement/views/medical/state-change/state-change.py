from django.shortcuts import render, get_object_or_404

from reimbursement.models.medical.medical import Medical


def state_change(request, medical_id):

    return render(request, 'reimbursement/medical/index.html', context)
