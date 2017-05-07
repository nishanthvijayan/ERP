from django.shortcuts import render

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense


def telephone_expense_show(request, telephone_expense_id):
    telephone_expense = TelephoneExpense.objects.filter(id=telephone_expense_id).first()
    context = {
        'telephone_expense': telephone_expense
    }
    print telephone_expense
    return render(request, 'reimbursement/telephone_expense/show.html', context)
