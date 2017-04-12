from django.shortcuts import render


def reimbursement_index(request):
    return render(request, 'reimbursement/index.html')


def reimbursement_track(request):
    return render(request, 'reimbursement/track.html')


def reimbursement_history(request):
    return render(request, 'reimbursement/history.html')
