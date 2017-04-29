from django.shortcuts import render


def reimbursement_requests_pending(request):
    return render(request, 'reimbursement/requests_pending.html')
