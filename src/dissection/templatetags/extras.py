from django import template


register = template.Library()


@register.filter
def split(value, arg):

    return value.split(arg)

@register.filter
def take_last(value):

    return value[-1]