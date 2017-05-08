from booking.models.mp_hall.mp_hall import MpHall
from booking.models.mp_hall.state import STATE

from django import template

register = template.Library()


@register.filter
def has_state_change_permission(user, mp_hall_id):
    """
    Function to check if a user is allowed to change state of the mp_hall form with id = mp_hall_id
    :param user: User
    :param mp_hall_id: MpHall.id
    :return: Bool
    """

    if MpHall.objects.filter(id=mp_hall_id).exists():
        employee = user.employee_set.all().first()
        if employee:
            if employee.department.hod.user.id == employee.user.id:
                if MpHall.objects.filter(id=mp_hall_id).filter(state=STATE.SUBMITTED).exists():
                    return True
                elif user.groups.filter(name='HindiTranslator').exists() \
                        and MpHall.objects.filter(id=mp_hall_id).filter(state=STATE.APPROVED_BY_HOD).exists():
                    return True
                elif user.groups.filter(name='R_AdministrativeDepartment').exists() \
                        and MpHall.objects.filter(id=mp_hall_id).filter(state=STATE.APPROVED_BY_DA).exists():
                    return True
                else:
                    return False
    else:
        return False
