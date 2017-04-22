from django.shortcuts import render


def reimbursement_submissions(request):
    return render(request, 'reimbursement/submissions.html')