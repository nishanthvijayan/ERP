from django.shortcuts import render


def telephone_expense_index(request):
    return render(request, 'reimbursement/index.html')
