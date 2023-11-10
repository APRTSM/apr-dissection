import json
from django import template
from ..utils import query


register = template.Library()

@register.simple_tag
def replace(string, old, new):
    return string.replace(old, new)

@register.simple_tag
def get_object_by_id(dataset, id):
    return query.get_object_by_id(dataset, id)
