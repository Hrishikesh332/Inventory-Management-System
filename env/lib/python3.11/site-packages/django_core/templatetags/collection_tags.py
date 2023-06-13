from __future__ import unicode_literals

import json

from django import template


register = template.Library()


@register.filter
def getitem(d, key):
    """
    Ability to access a dictionary keys based on a dynamic key:

    Usage:

     my_vals = {'hello': 'world', 'testing': 'again'}

     {{ my_vals|get:'hello' }}

     would return "world"
    """
    if not isinstance(d, dict):
        return ''

    return d.get(key, '')


@register.filter
def attr(obj, attr):
    """
    Does the same thing as getattr.

    getattr(obj, attr, '')
    """
    if not obj or not hasattr(obj, attr):
        return ''

    return getattr(obj, attr, '')


@register.filter
def jsondumps(obj):
    """Turns a json object into a string."""
    return json.dumps(obj)


@register.filter
def make_iterable(obj):
    """Make an object iterable.

    >>> make_iterable(obj='hello')
    ('hello',)
    >>> make_iterable(obj=None)
    ()
    """
    if not obj:
        return tuple()

    if isinstance(obj, (list, tuple, set)):
        return obj

    return (obj,)
