from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Function to check if a user is in group or not
    :param user: User
    :param group_name: Group
    :return: Bool
    """
    return user.groups.filter(name=group_name).exists()
