from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django_fsm import can_proceed
from django.contrib import messages
from django.db import transaction, IntegrityError

from reimbursement.models.telephone_expense.state import STATE

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense
from reimbursement.models.telephone_expense.telephone_expense_transition_history \
    import TelephoneExpenseTransitionHistory

from reimbursement.forms.telephone_expense.telephone_expense import TelephoneExpenseForm


def generate_state_change_dealing_assistant(request, telephone_expense_id):
    telephone_expense = get_object_or_404(TelephoneExpense, id=telephone_expense_id)
    if request.method == 'POST':
        telephone_expense_form = TelephoneExpenseForm(data=request.POST, instance=telephone_expense)
        if telephone_expense_form.is_valid():
            if request.POST.get('APPROVED_BY_DA', False):
                if telephone_expense_form.save():
                    try:
                        with transaction.atomic():
                            if not can_proceed(telephone_expense.approve_by_da):
                                raise PermissionDenied
                            transition = TelephoneExpenseTransitionHistory.objects.create(
                                state_from=STATE.SUBMITTED,
                                state_to=STATE.APPROVED_BY_DA,
                                remarks=request.POST.get('state-change-remarks', ''),
                                approved_by=request.user,
                                telephone_expense=telephone_expense
                            )
                            transition.save()
                            telephone_expense.approve_by_da()
                            telephone_expense.save()
                            messages.success(request, 'Request for Telephone Expense reimbursement #'
                                             + str(telephone_expense_id)
                                             + ' successfully approved!'
                                             )
                            return redirect('reimbursement:telephone-expense-show', telephone_expense_id)
                    except IntegrityError:
                        messages.error(request, 'There was an error approving the reimbursement request')
                else:
                        messages.error(request, 'Please resolve the errors below and try again')
            elif request.POST.get('REJECTED_BY_DA', False):
                try:
                    with transaction.atomic():
                        if not can_proceed(telephone_expense.reject_by_da):
                            raise PermissionDenied
                        transition = TelephoneExpenseTransitionHistory.objects.create(
                            state_from=STATE.SUBMITTED,
                            state_to=STATE.REJECTED_BY_DA,
                            remarks=request.POST.get('state-change-remarks', ''),
                            approved_by=request.user,
                            telephone_expense=telephone_expense
                        )
                        transition.save()
                        telephone_expense.reject_by_da()
                        telephone_expense.save()
                        messages.success(request, 'Request for Telephone Expense reimbursement #' + str(
                            telephone_expense_id)
                                         + ' successfully rejected!')
                        return redirect('reimbursement:telephone-expense-show', telephone_expense_id)
                except IntegrityError:
                    messages.error(request, 'There was an error rejecting the reimbursement request')
    else:
        telephone_expense_form = TelephoneExpenseForm(instance=telephone_expense)
    context = {
        'telephone_expense': telephone_expense,
        'telephone_expense_form': telephone_expense_form
    }
    return render(request, 'reimbursement/telephone_expense/state_change/role_based/dealing_assistant.html', context)
