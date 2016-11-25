from django import template

register = template.Library()


@register.filter(name='values_list')
def values_list(query_set, field):
    return list(query_set.values_list(field, flat=True))
