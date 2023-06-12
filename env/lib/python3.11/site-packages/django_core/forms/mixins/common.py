from __future__ import unicode_literals

from django import forms
from django.forms.util import ErrorDict
from django.forms.widgets import HiddenInput


class PrefixFormMixin(forms.ModelForm):
    """Form mixin for prefix.  Handles prefixing for new vs existing instances
    for forms.  Many forms rendered to a page will require a prefix to maintain
    uniqueness with rendering.  This stores the prefix used to assist with
    this.

    The consuming form must implement the following two fields:

    1. ``default_instance_prefix``: this is the prefix to use when an exsiting
        instance is used (already exists in the database).
    2. ``default_new_prefix``: this is the prefix to use when a new instance
        is being created.
    """
    # TODO: why is this a form field and is it used ever?
    form_prefix = forms.CharField(max_length=200, required=False,
                                  widget=HiddenInput)

    default_instance_prefix = None
    default_new_prefix = None

    def __init__(self, prefix=None, use_default_prefix=False, *args, **kwargs):

        if prefix is None and use_default_prefix:
            instance = kwargs.get('instance')
            prefix = self.get_default_prefix(instance=instance)

        super(PrefixFormMixin, self).__init__(prefix=prefix, *args, **kwargs)

    def get_default_prefix(self, instance=None):
        """Gets the prefix for this form.

        :param instance: the form model instance.  When calling this method
            directly this should almost always stay None so it looks for
            self.instance.
        """
        if instance is None and hasattr(self, 'instance'):
            instance = self.instance

        if instance and instance.id is not None:
            # it's an existing instance, use the instance prefix
            instance_prefix = self.default_instance_prefix
            if instance_prefix is None:
                instance_prefix = self.__class__.__name__.lower() + 'i-'

            return '{0}{1}'.format(instance_prefix,
                                   instance.id)

        if self.default_new_prefix is not None:
            return self.default_new_prefix

        return self.__class__.__name__.lower() + 'new-'


class DeleteFormMixin(forms.ModelForm):
    """Delete form mixin when a delete field is needed.  This also prevents
    a form from saving when the delete field is set to true since it should be
    deleted.
    """

    delete = forms.BooleanField(initial=False, required=False,
                                widget=forms.HiddenInput)

    def is_valid(self):
        if hasattr(self, 'cleaned_data') and \
           self.cleaned_data.get('delete') is True:
            return True

        return super(DeleteFormMixin, self).is_valid()

    def clean(self):
        cleaned_data = super(DeleteFormMixin, self).clean()

        # If this object is set to be deleted, validation doesn't matter
        # because the object will be delete anyway so remove all errors so it
        # passes validation.

        if self.cleaned_data.get('delete') is True:
            self._errors = ErrorDict()

        return cleaned_data

    def save(self, *args, **kwargs):
        if self.cleaned_data.get('delete') is True:
            # saving is not allowed for forms that have delete set to true
            return None

        return super(DeleteFormMixin, self).save(*args, **kwargs)
