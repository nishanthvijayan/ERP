from django.shortcuts import render, get_object_or_404

from reimbursement.models.medical.medical import Medical


def show(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    context = {
        'medical': medical
    }
    return render(request, 'reimbursement/medical/index.html', context)
