from booking.models.mp_hall.mp_hall import MpHall
from booking.models.mp_hall.state import STATE

from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """
    Function to check if a user is in group or not
    :param user: User
    :param group_name: Group
    :return: Bool
    """
    return user.groups.filter(name=group_name).exists()
