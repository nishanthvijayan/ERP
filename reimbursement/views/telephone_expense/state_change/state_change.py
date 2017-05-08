from django.http import Http404

from reimbursement.models.telephone_expense.state import STATE

from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense

from role_based.dealing_assistant import generate_state_change_dealing_assistant
from role_based.deputy_registrar import generate_state_change_deputy_registrar
from role_based.senior_audit_officer import generate_state_change_senior_audit_officer
from role_based.registrar import generate_state_change_registrar
from role_based.junior_accounting_officer \
    import generate_state_change_junior_accounting_officer


def state_change(request, telephone_expense_id):
    """
    Generates view for changing the state of the reimbursement request
    :param request:
    :param telephone_expense_id:
    :return: HttpResponse Object
    """
    if TelephoneExpense.objects.filter(id=telephone_expense_id).exists():

        if request.user.groups.filter(name='AAO_AccountsDepartment').exists() \
                and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.SUBMITTED).exists():
            return generate_state_change_dealing_assistant(request, telephone_expense_id)

        elif request.user.groups.filter(name='DR_AccountsDepartment').exists() \
                and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(
                    state=STATE.APPROVED_BY_DA
                ).exists():

            return generate_state_change_deputy_registrar(request, telephone_expense_id)

        elif request.user.groups.filter(name='SrAO_AuditDepartment').exists() \
                and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(
                    state=STATE.APPROVED_BY_DR
                ).exists():
            return generate_state_change_senior_audit_officer(request, telephone_expense_id)

        elif request.user.groups.filter(name='R_AdministrativeDepartment').exists() \
                and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(
                    state=STATE.APPROVED_BY_SrAO
                ).exists():
            return generate_state_change_registrar(request, telephone_expense_id)

        elif request.user.groups.filter(name='JrAO_AccountsDepartment').exists() \
                and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.APPROVED_BY_R).exists():
            return generate_state_change_junior_accounting_officer(request, telephone_expense_id)

        else:
            raise Http404

    else:
        raise Http404
