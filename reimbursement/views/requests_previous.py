from django.shortcuts import render


def reimbursement_requests_previous(request):
    return render(request, 'reimbursement/requests_previous.html')
