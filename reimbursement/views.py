from django.shortcuts import render


def reimbursement_index(request):
    return render(request, 'reimbursement/index.html')


def reimbursement_track(request):
    return render(request, 'reimbursement/track.html')


def reimbursement_requests_pending(request):
    return render(request, 'reimbursement/requests_pending.html')


def reimbursement_requests_previous(request):
    return render(request, 'reimbursement/requests_previous.html')
