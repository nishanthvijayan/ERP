from django.shortcuts import render, get_object_or_404
from django.http import Http404

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense


def telephone_expense_show(request, telephone_expense_id):
    telephone_expense = get_object_or_404(TelephoneExpense, id=telephone_expense_id)
    if request.user.groups.filter(name='Reimbursement_Telephone_Expense_Change_State').exists() \
            or TelephoneExpense.objects.filter(id=telephone_expense_id) \
                    .filter(employee__user_id=request.user.id) \
                    .exists():
        context = {
            'telephone_expense': telephone_expense
        }
        return render(request, 'reimbursement/telephone_expense/show.html', context)
    else:
        raise Http404
