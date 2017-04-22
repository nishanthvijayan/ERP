from django.shortcuts import render


def reimbursement_index(request):
    return render(request, 'reimbursement/index.html')