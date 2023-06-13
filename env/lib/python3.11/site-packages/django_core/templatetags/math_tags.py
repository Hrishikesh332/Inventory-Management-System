from __future__ import unicode_literals

from django import template


register = template.Library()


@register.filter
def substract(value, subtract_by):
    """
    Get the absolute value for "value".  This template tag is a wrapper for
    pythons "abs(...)" method.

    Usage:

    >>> absolute(5, 2)
    3
    """
    return value - subtract_by


@register.filter
def multiply(value, multiplier):
    """
    Multiplies two values together.

    Usage:

    >>> multiply(5, 2)
    10
    """
    return value * multiplier


@register.filter
def divide(numerator, denominator):
    """
    Divides two values from each other.

    Usage:

    >>> absolute(-5)
    5
    """
    return numerator / denominator


@register.filter
def absolute(value):
    """
    Get the absolute value for "value".  This template tag is a wrapper for
    pythons "abs(...)" method.

    Usage:

    >>> absolute(-5)
    5
    """
    try:
        return abs(value)
    except:
        return value
