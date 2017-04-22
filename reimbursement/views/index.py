from django.shortcuts import render

from reimbursement.models.medical import Medical


def reimbursement_index(request):
    medical_list = Medical.objects.all()
    context = {
        'medical': medical_list
    }
    return render(request, 'reimbursement/index.html', context)