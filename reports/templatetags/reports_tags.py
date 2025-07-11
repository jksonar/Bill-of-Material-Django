from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def selectattr(value, arg):
    """Filter a list of objects by a given attribute."""
    return [getattr(obj, arg) for obj in value if hasattr(obj, arg)]