from django import template

register = template.Library()

@register.filter
def truncate_chars(value, num):
    if len(value) > num:
        return value[:num] + '...'
    return value

@register.simple_tag
def increment_index(index):
    return index + 1

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except IndexError:
        return None