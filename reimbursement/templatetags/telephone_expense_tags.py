from reimbursement.models.telephone_expense.telephone_expense import TelephoneExpense
from reimbursement.models.telephone_expense.state import STATE

from django import template

register = template.Library()


@register.filter
def has_state_change_permission(user, telephone_expense_id):
    """
    Function to check if a user is allowed to change state of the telephone expense reimbursement
    request with id = telephone_expense_id
    :param user: User
    :param telephone_expense_id: TelephoneExpense.id
    :return: Bool
    """
    if user.groups.filter(name='AAO_AccountsDepartment').exists() \
            and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.SUBMITTED).exists():
        return True
    elif user.groups.filter(name='DR_AccountsDepartment').exists() \
            and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.APPROVED_BY_DA).exists():
        return True
    elif user.groups.filter(name='SrAO_AuditDepartment').exists() \
            and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.APPROVED_BY_DR).exists():
        return True
    elif user.groups.filter(name='R_AdministrativeDepartment').exists() \
            and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.APPROVED_BY_SrAO).exists():
        return True
    elif user.groups.filter(name='JrAO_AccountsDepartment').exists() \
            and TelephoneExpense.objects.filter(id=telephone_expense_id).filter(state=STATE.APPROVED_BY_R).exists():
        return True
    else:
        return False
