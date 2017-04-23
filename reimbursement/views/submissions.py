from django.shortcuts import render

from reimbursement.models.medical import Medical


def reimbursement_submissions(request):
    medical_list = Medical.objects.all()
    context = {
        'medicals': medical_list
    }
    return render(request, 'reimbursement/submissions.html', context)