from __future__ import unicode_literals

import ast
import json

from django import forms
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.encoding import smart_text
from django.utils.six import string_types
from django.utils.six import with_metaclass
from django.utils.translation import ugettext as _


class ListField(with_metaclass(models.SubfieldBase, models.CharField)):
    """Model field for python lists.

    Note: this extends from CharField so all restrictions apply to this model
    field that apply to CharField (i.e. max_length)
    """
    description = "Stores a python list"
    form_class = forms.CharField
    choices_form_class = forms.TypedMultipleChoiceField

    default_error_messages = {
        'invalid_list': _("'%(value)s' value must be a list type."),
        'invalid_choice': _("'%(value)s' is not a valid choice.")
    }

    def __init__(self, max_length=2000, form_class=None,
                 choices_form_class=None, *args, **kwargs):
        """
        :param max_length: this is the total length the string could be for all
            characters in the string. So, a field value of:

            ['hello', 'world'] == length of 18
        :param form_class: the form field class to user for this field.
        """
        if form_class:
            self.default_field_class = form_class

        if choices_form_class:
            self.choices_form_class = choices_form_class

        super(ListField, self).__init__(max_length=max_length, *args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value

        if not value:
            return []

        if isinstance(value, list):
            if len(value) == 0 or not self.choices:
                return value

            # Validate choices
            valid_choices = tuple(choice[0] for choice in self.choices)

            for item in value:
                if item not in valid_choices:
                    raise ValidationError(
                        self.error_messages['invalid_choice'],
                        code='invalid_choice',
                        params={'value': item}
                    )

            return value

        try:
            return ast.literal_eval(value)
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid_list'],
                code='invalid_list',
                params={'value': value}
            )

    def get_prep_value(self, value):
        if value is None:
            return value

        if not isinstance(value, list):
            raise ValidationError(
                self.error_messages['invalid_list'],
                code='invalid_list',
                params={'value': value}
            )

        return smart_text(value)

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        """Make the default formfield a CommaSeparatedListField."""
        defaults = {
            'form_class': form_class or self.get_form_class()
        }
        defaults.update(kwargs)

        return super(ListField, self).formfield(**defaults)

    def get_form_class(self):
        """Gets the form field class to user for the field."""
        return self.form_class

    def get_choices_form_class(self):
        return self.choices_form_class

    def validate(self, value, model_instance, **kwargs):
        """This follows the validate rules for choices_form_class field used.
        """
        self.get_choices_form_class().validate(value, model_instance, **kwargs)


class IntegerListField(with_metaclass(models.SubfieldBase, ListField)):
    """Wrapper around ListField ensuring all values are integers."""

    default_error_messages = {
        'invalid_integers': _('All values in list "%(value)s" must be of '
                              'integer types.'),
        'invalid_out_of_range_min': _('"%(value)s" out of range. Must be '
                                      'greater than or equal to %(min)s'),
        'invalid_out_of_range_max': _('"%(value)s" out of range. Must be '
                                      'less than or equal to %(max)s')
    }

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        """
        :param min_value: the minimum value that can be in the list
        :param max_value: the maximum value that can be in the list
        """
        self.min_value = min_value
        self.max_value = max_value
        super(IntegerListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        val = super(IntegerListField, self).to_python(value)

        if isinstance(val, list):

            try:
                val = [int(item) for item in val]
            except:
                raise ValidationError(
                    self.error_messages['invalid_integers'],
                    code='invalid_integers',
                    params={'value': val}
                )

            # Validate that all items in the list are integers.
            for item in val:

                if self.min_value is not None and item < self.min_value:
                    raise ValidationError(
                        self.error_messages['invalid_out_of_range_min'],
                        code='invalid_out_of_range_min',
                        params={'value': item, 'min': self.min_value}
                    )

                if self.max_value is not None and item > self.max_value:
                    raise ValidationError(
                        self.error_messages['invalid_out_of_range_max'],
                        code='invalid_out_of_range_max',
                        params={'value': item, 'max': self.max_value}
                    )

        return val

    def get_prep_value(self, value):

        prepped_value = super(IntegerListField, self).get_prep_value(value)

        if value:
            # Remove all spaces from the stored string since all items will be
            # integers anyway and spaces aren't needed.
            return prepped_value.replace(' ', '')

        return prepped_value


class JSONField(with_metaclass(models.SubfieldBase, models.TextField)):
    """Simple JSON field that stores python structures as JSON strings
    on database.

    Borrowed from django-social-auth :):

    https://github.com/omab/django-social-auth/blob/master/social_auth/fields.py

    """
    def __init__(self, *args, **kwargs):
        default = kwargs.get('default', None)
        if default is None:
            kwargs['default'] = '{}'
        models.TextField.__init__(self, *args, **kwargs)

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if isinstance(value, dict):
            return value

        if self.blank and not value:
            return None

        if isinstance(value, string_types):
            try:
                return json.loads(value)
            except Exception as e:
                raise ValidationError(str(e))

        return value

    def validate(self, value, model_instance):
        """Check value is a valid JSON string, raise ValidationError on
        error."""
        if isinstance(value, string_types):
            super(JSONField, self).validate(value, model_instance)
            try:
                json.loads(value)
            except Exception as e:
                raise ValidationError(str(e))

    def get_prep_value(self, value):
        """Convert value to JSON string before save"""
        try:
            return json.dumps(value, cls=DjangoJSONEncoder)
        except Exception as e:
            raise ValidationError(str(e))

    def value_to_string(self, obj):
        """Return value from object converted to string properly"""
        return smart_text(self.get_prep_value(self._get_val_from_obj(obj)))
