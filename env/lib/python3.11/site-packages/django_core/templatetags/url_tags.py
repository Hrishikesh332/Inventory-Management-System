from __future__ import unicode_literals

from django.template import Library

from ..html.builders import build_link


register = Library()


@register.filter
def get_absolute_url_link(obj, text=None):
    """Gets the absolute url html link for the object.

    Usage:

    {{ obj|get_absolute_url_link:"Some Text" }}

    Would return:

    u'<a href="{{ THE OBJ ABSOLUTE URL }}">{{ TEXT THAT WAS PASSED IN }}</a>'
    """
    return absolute_url_link(obj=obj, text=text)


@register.simple_tag
def absolute_url_link(obj, **kwargs):
    if hasattr(obj, 'get_absolute_url_link'):
        return obj.get_absolute_url_link(**kwargs)

    absolute_url = obj.get_absolute_url()
    return build_link(href=absolute_url, **kwargs)


@register.filter
def get_edit_url_link(obj, text=None):
    """Gets the absolute url html link for the object.

    Usage:

    {{ obj|get_edit_url_link:"Some Text" }}

    Would return:

    u'<a href="{{ THE OBJ EDIT URL }}">{{ TEXT THAT WAS PASSED IN }}</a>'
    """
    return edit_url_link(obj=obj, text=text)


@register.simple_tag
def edit_url_link(obj, **kwargs):
    """This method assumes that the "get_delete_url_link" method has been
    implemented on the obj.
    """
    if hasattr(obj, 'get_edit_url_link'):
        return obj.get_edit_url_link(**kwargs)

    edit_url = obj.get_edit_url()
    return build_link(href=edit_url, **kwargs)


@register.filter
def get_delete_url_link(obj, text=None):
    """Gets the absolute url html link for the object.
    """
    return delete_url_link(obj=obj, text=text)


@register.simple_tag
def delete_url_link(obj, **kwargs):
    """This method assumes that the "get_delete_url_link" method has been
    implemented on the obj.
    """
    if hasattr(obj, 'get_delete_url_link'):
        return obj.get_delete_url_link(**kwargs)

    delete_url = obj.get_delete_url()
    return build_link(href=delete_url, **kwargs)
