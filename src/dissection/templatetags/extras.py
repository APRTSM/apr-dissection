import json
from django import template
from ..utils import query


register = template.Library()

@register.simple_tag
def replace(string, old, new):
    return string.replace(old, new)

@register.filter
def get_value_by_key(dictionary, key):
    return dictionary.get(key)
    
@register.simple_tag
def get_object_by_id(dataset, id):
    return query.get_object_by_id(dataset, id)

@register.simple_tag
def get_objects_by_feature(dataset, feature, value):
    return query.get_objects_by_feature(dataset, feature, value)
