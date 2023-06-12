from __future__ import unicode_literals


def make_obj_list(obj_or_objs):
    """This method will take an object or list of objects and ensure a list is
    returned.

    Example:

    >>> make_obj_list('hello')
    ['hello']
    >>> make_obj_list(['hello', 'world'])
    ['hello', 'world']
    >>> make_obj_list(None)
    []

    """
    if not obj_or_objs:
        return []

    if not isinstance(obj_or_objs, (list, tuple)):
        return [obj_or_objs]

    return obj_or_objs
