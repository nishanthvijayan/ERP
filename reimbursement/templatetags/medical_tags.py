from reimbursement.models.medical.medical import Medical
from reimbursement.models.medical.state import STATE

from django import template

register = template.Library()


@register.filter
def has_state_change_permission(user, medical_id):
    """
    Function to check if a user is allowed to change state of the medical form with id = medical_id
    :param user: User
    :param medical_id: Medical.id
    :return: Bool
    """
    if user.groups.filter(name='AAO_AccountsDepartment').exists() \
            and Medical.objects.filter(id=medical_id).filter(state=STATE.SUBMITTED).exists():
        return True
    elif user.groups.filter(name='MS_HealthCareDepartment').exists() \
            and Medical.objects.filter(id=medical_id).filter(state=STATE.VERIFIED_BY_DA).exists():
        return True
    elif user.groups.filter(name='DR_AccountsDepartment').exists() \
            and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_MS).exists():
        return True
    elif user.groups.filter(name='SrAO_AuditDepartment').exists() \
            and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_DR).exists():
        return True
    elif user.groups.filter(name='R_AdministrativeDepartment').exists() \
            and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_SrAO).exists():
        return True
    elif user.groups.filter(name='JrAO_AccountsDepartment').exists() \
            and Medical.objects.filter(id=medical_id).filter(state=STATE.APPROVED_BY_R).exists():
        return True
    else:
        return False
