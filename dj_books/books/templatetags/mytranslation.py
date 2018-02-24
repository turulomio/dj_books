from django import template

from django.utils.translation import activate

register = template.Library()

@register.simple_tag
def set_language(value):
    return activate(value.lower())
