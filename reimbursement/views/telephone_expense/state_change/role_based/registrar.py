from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django_fsm import can_proceed
from django.contrib import messages
from django.db import transaction, IntegrityError

from reimbursement.models.telephone_expense.state import STATE

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense
from reimbursement.models.telephone_expense.telephone_expense_transition_history \
    import TelephoneExpenseTransitionHistory


def generate_state_change_registrar(request, telephone_expense_id):
    """
    Generates view for registrar i.e R for changing of states(Approve, Reject)
    This function assumes current user is authenticated as R
    :param request: HttpRequestObject
    :param telephone_expense_id:
    :return: HttpResponseObject
    """
    telephone_expense = get_object_or_404(TelephoneExpense,id=telephone_expense_id)
    form_errors = {}
    if request.method == 'POST':
        if request.POST.get('APPROVED_BY_R', False):
            try:
                with transaction.atomic():
                    if not can_proceed(telephone_expense.approve_by_r):
                        raise PermissionDenied
                    transition = TelephoneExpenseTransitionHistory.objects.create(
                        state_from=STATE.APPROVED_BY_SrAO,
                        state_to=STATE.APPROVED_BY_R,
                        remarks=request.POST.get('state-change-remarks', ''),
                        approved_by=request.user,
                        telephone_expense=telephone_expense
                    )
                    transition.save()
                    telephone_expense.approve_by_r()
                    telephone_expense.save()
                    messages.success(request, 'Request for Telephone Expense reimbursement #' + str(telephone_expense_id)
                                     + ' successfully approved!')
                    return redirect('reimbursement:telephone-expense-show', telephone_expense_id)
            except IntegrityError:
                messages.error(request, 'There was an error approving the reimbursement request')
            else:
                messages.error(request, 'Please resolve the errors below and try again')
        elif request.POST.get('REJECTED_BY_R', False):
            try:
                with transaction.atomic():
                    if not can_proceed(telephone_expense.reject_by_r):
                        raise PermissionDenied
                    transition = TelephoneExpenseTransitionHistory.objects.create(
                        state_from=STATE.APPROVED_BY_SrAO,
                        state_to=STATE.REJECTED_BY_R,
                        remarks=request.POST.get('state-change-remarks', ''),
                        approved_by=request.user,
                        telephone_expense=telephone_expense
                    )
                    transition.save()
                    telephone_expense.reject_by_r()
                    telephone_expense.save()
                    messages.success(request, 'Request for Telephone Expense reimbursement #' + str(telephone_expense_id)
                                                        + ' successfully rejected!')
                    return redirect('reimbursement:telephone-expense-show', telephone_expense_id)
            except IntegrityError:
                messages.error(request, 'There was an error rejecting the reimbursement request')
            else:
                messages.error(request, 'Please resolve the errors below and try again')
    else:
        pass
    context = {
        'form_errors': form_errors,
        'telephone_expense': telephone_expense
    }
    return render(request, 'reimbursement/telephone_expense/state_change/role_based/registrar.html', context)
