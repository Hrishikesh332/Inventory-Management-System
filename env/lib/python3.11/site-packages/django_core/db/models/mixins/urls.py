from __future__ import unicode_literals

from django.db import models
from django_core.html.builders import build_link


class AbstractUrlLinkModelMixin(models.Model):
    """Mixin for accessing the links for the models.  This requires the object
    to have already implemented the following methods:

    To override the model field used for the absolute url, override the
    following method:

    * get_link_text_field()

    to the model and that field will be used for the text.

    * get_absolute_url - returns the absolute link to the object.
    * get_edit_url - returns the link to edit the object
    * get_delete_url - return the link to delete the object.
    """

    class Meta:
        abstract = True

    def get_absolute_url_link(self, text=None, cls=None, icon_class=None,
                              **attrs):
        """Gets the html link for the object."""
        if text is None:
            text = getattr(self, self.get_link_text_field(), self.id)

        return build_link(href=self.get_absolute_url(),
                          text=text,
                          cls=cls,
                          icon_class=icon_class,
                          **attrs)

    def get_edit_url_link(self, text=None, cls=None, icon_class=None,
                          **attrs):
        """Gets the html edit link for the object."""
        if text is None:
            text = 'Edit'

        return build_link(href=self.get_edit_url(),
                          text=text,
                          cls=cls,
                          icon_class=icon_class,
                          **attrs)

    def get_delete_url_link(self, text=None, cls=None, icon_class=None,
                            **attrs):
        """Gets the html delete link for the object."""
        if text is None:
            text = 'Delete'

        return build_link(href=self.get_delete_url(),
                          text=text,
                          cls=cls,
                          icon_class=icon_class,
                          **attrs)

    def get_link_text_field(self):
        """This returns the field name to use for the absolute url."""
        return 'id'
