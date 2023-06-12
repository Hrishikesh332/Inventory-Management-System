from __future__ import unicode_literals

from copy import deepcopy

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.forms.fields import ChoiceField
from django.forms.fields import DecimalField
from django.forms.fields import MultiValueField
from django.utils.translation import ugettext as _
from django_core.forms.widgets import ChoiceAndCharInputWidget

from .widgets import MultipleDecimalInputWidget


class CharFieldStripped(CharField):
    """Wrapper around CharField that strips whitespace from the CharField when
    validating so .strip() doesn't have to be called every time you validate
    the field's data.
    """

    def clean(self, value):
        if value:
            value = value.strip()

        return super(CharFieldStripped, self).clean(value)


class CommaSeparatedListField(CharFieldStripped):
    """Form field that takes a string and converts into a list of strings."""

    def __init__(self, max_list_length=None, max_list_length_error_msg=None,
                 *args, **kwargs):
        """
        :params max_list_length: the max number of items in the list.  If None,
            there is no limit.
        :params max_list_length_error_msg: if the max limit is reached, this is
            the error message that will display.
        """
        super(CommaSeparatedListField, self).__init__(*args, **kwargs)
        self.max_list_length = max_list_length
        self.max_list_length_error_msg = max_list_length_error_msg

    def validate(self, value):
        super(CommaSeparatedListField, self).validate(value)

        if (self.max_list_length is not None and
            len(value) > self.max_list_length):

            if self.max_list_length_error_msg:
                raise ValidationError(self.max_list_length_error_msg)

            raise ValidationError(_(
                'Maximum number of items is {0}. There are currently {1} items '
                'listed.').format(self.max_list_length, len(value)))

    def to_python(self, value):
        value = super(CharFieldStripped, self).to_python(value)
        return [item.strip() for item in value.split(',') if item.strip()]


class CommaSeparatedIntegerListField(CommaSeparatedListField):
    """Comma Separated Integer list field."""
    # TODO: this should honor:
    #    max_value (each item in the list can't be > this value)
    #    min_value (each item in the list can't be < this value)
    #    max_length (could be the number of items in the list)

    def to_python(self, value):
        value = super(CommaSeparatedIntegerListField, self).to_python(value)

        if isinstance(value, (list, tuple)):
            # Ensure all values are integers
            try:
                value = [int(item) for item in value]
            except:
                raise ValidationError('All values in list must be whole '
                                      'numbers.')
        return value


class MultipleDecimalField(MultiValueField):
    """A field with multiple decimal fields that should be converted to single
    line.

    Example response values:

    - "5px 0 5px 4px"
    """
    widget = MultipleDecimalInputWidget

    def __init__(self, num_inputs=2, value_suffix='', *args, **kwargs):
        """

        :param value_suffix: the suffix to append to the end of the decimal
            field. Default is nothing.
        """
        self.num_inputs = num_inputs
        self.value_suffix = value_suffix
        fields = [DecimalField(required=False)
                  for i in range(num_inputs)]
        widget = self.widget(num_inputs=num_inputs)
        super(MultipleDecimalField, self).__init__(fields=fields,
                                                   widget=widget,
                                                   *args, **kwargs)

    def clean(self, value):
        """Validates that the input can be converted to a list of decimals."""
        if not value:
            return None

        # if any value exists, then add "0" as a placeholder to the remaining
        # values.
        if isinstance(value, list) and any(value):
            for i, item in enumerate(value):
                if not item:
                    value[i] = '0'

        return super(MultipleDecimalField, self).clean(value)

    def compress(self, data_list):
        # This should be formatted to a string 5px 5px 2px 2px
        if not data_list:
            return None

        values = deepcopy(data_list)

        for index, value in enumerate(values):
            if value and float(value).is_integer():
                value = int(value)

            if value:
                values[index] = '{0}{1}'.format(value, self.value_suffix)
            else:
                values[index] = '0'

        return ' '.join(values)

    def to_python(self, value):
        """Validates that the input can be converted to a list of decimals."""
        if not value:
            return None

        if isinstance(value, list):
            for index, position_val in enumerate(value):
                val = super(MultipleDecimalField, self).to_python(position_val)
                value[index] = val

        return value


class ChoiceAndCharField(MultiValueField):
    widget = ChoiceAndCharInputWidget

    def __init__(self, choices=None, widget_css_class='', *args, **kwargs):

        if 'widget' in kwargs:
            self.widget = kwargs.pop('widget')

        fields = (
            ChoiceField(choices=choices, required=False),
            CharField(required=False)
        )

        widget_kwargs = {
            'choices': choices
        }

        if widget_css_class:
            css_class = 'choice-and-char-widget {0}'.format(widget_css_class)
            widget_kwargs['widget_css_class'] = css_class

        widget = self.widget(**widget_kwargs)
        super(ChoiceAndCharField, self).__init__(fields=fields,
                                                 widget=widget,
                                                 *args,
                                                 **kwargs)

    def compress(self, data_list):
        return data_list
