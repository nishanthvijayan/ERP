from django.shortcuts import render


def reimbursement_index(request):
    return render(request, 'reimbursement/index.html')


def reimbursement_tracking(request):
    return render(request, 'reimbursement/tracking.html')


def reimbursement_history(request):
    return render(request, 'reimbursement/history.html')
