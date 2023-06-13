from __future__ import unicode_literals

from django.utils.html import escape
from django.utils.safestring import mark_safe


def build_link(href, text, cls=None, icon_class=None, **attrs):
    """Builds an html link.

    :param href: link for the anchor element
    :param text: text for the anchor element
    :param attrs: other attribute kwargs

    >>> build_link('xyz.com', 'hello', 'big')
    u'<a href="xyz.com" class="big">hello</a>'
    >>> build_link('xyz.com', 'hello', 'big', 'fa fa-times')
    u'<a href="xyz.com" class="big"><i class="fa fa-times"></i> hello</a>'
    """
    return build_html_element(tag='a',
                              text=text,
                              href=href,
                              cls=cls,
                              icon_class=icon_class,
                              **attrs)


def build_html_element(tag, text=None, icon_class=None, cls=None, **kwargs):
    """Builds an html element.

    :param tag: the html tag to build ('a', 'div', 'img', etc)
    :param icon_class: the class to apply to an icon element.  This only
        applies to elements that allow a closing tag.
    :param cls: the css class to apply to the tag.  This can also be passed
        in as a kwarg as "class".

    >>> build_html_element(tag='a', href='someurl.com', text='hello')
    '<a href='someurl.com'>hello</a>'
    """
    if cls is not None:
        kwargs['class'] = cls

    tag_attrs = ' '.join(['{0}="{1}"'.format(k, v) for k, v in kwargs.items()])

    tag_content = '{tag} {tag_attrs}'.format(tag=tag, tag_attrs=tag_attrs)

    if tag in ('img', 'input', 'hr', 'br'):
        return mark_safe('<{tag_content} />'.format(tag_content=tag_content))

    icon = '<i class="{0}"></i> '.format(icon_class) if icon_class else ''

    return mark_safe('<{tag_content}>{icon}{text}</{tag}>'.format(
        tag_content=tag_content,
        icon=icon,
        tag=tag,
        text=escape(text) or '')
    )
