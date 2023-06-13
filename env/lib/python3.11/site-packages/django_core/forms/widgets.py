from __future__ import unicode_literals

from datetime import date
from datetime import datetime

from django.forms.widgets import DateInput
from django.forms.widgets import DateTimeInput
from django.forms.widgets import MultiWidget
from django.forms.widgets import Select
from django.forms.widgets import TextInput
from django.utils.six import string_types


try:
    # django >= 1.6
    from django.forms.widgets import NumberInput
except ImportError:
    # django < 1.6 doesn't have the NumberInput class
    class NumberInput(TextInput):
        input_type = 'number'


class ExtendedMultiWidget(MultiWidget):
    """Wrapper around the MultiWidget that allow for putting a custom css class
    around multiple widgets.
    """

    def __init__(self, widget_css_class=None, **kwargs):
        """
        :param widget_css_class: the string css class(es) to put around the
            entire widget.
        """
        self.widget_css_class = widget_css_class
        super(ExtendedMultiWidget, self).__init__(**kwargs)

    def format_output(self, *args, **kwargs):
        output = super(ExtendedMultiWidget, self).format_output(*args,
                                                                **kwargs)
        return '<div class="{0}">{1}</div>'.format(
            self.widget_css_class,
            output
        )


class MultipleDecimalInputWidget(ExtendedMultiWidget):
    """Renders an input with 4 decimal fields."""

    def __init__(self, attrs=None, widgets=None, num_inputs=4, value_suffix='',
                 widget_css_class='horizontal-widget multi-decimal-widget',
                 **kwargs):
        self.num_inputs = num_inputs
        self.value_suffix = value_suffix

        if not attrs:
            attrs = {}

        self.get_widget_css_class(attrs)

        if widgets is None:
            widgets = tuple([NumberInput() for w in range(num_inputs)])

        super(MultipleDecimalInputWidget, self).__init__(
            widgets=widgets,
            attrs=attrs,
            widget_css_class=widget_css_class,
            **kwargs
        )

    def decompress(self, value):
        if value and self.value_suffix and isinstance(value, string_types):
            value = value.replace(self.value_suffix, '')

        if value:
            return value.split(' ')

        return [None for i in range(self.num_inputs)]

    def get_widget_css_class(self, attrs):
        """Gets the class for the widget."""
        size_class = 'size-{0}'.format(self.num_inputs)

        if 'class' in attrs:
            attrs['class'] += ' {0}'.format(size_class)
        else:
            attrs['class'] = size_class


class ChoiceAndCharInputWidget(ExtendedMultiWidget):
    """Renders choice field and char field next to each other."""

    def __init__(self, choices=None, attrs=None, widgets=None,
                 widget_css_class='choice-and-char-widget', **kwargs):

        if not attrs:
            attrs = {}

        if not widgets:
            widgets = (
                Select(choices=choices),
                TextInput()
            )

        super(ChoiceAndCharInputWidget, self).__init__(
            widgets=widgets,
            attrs=attrs,
            widget_css_class=widget_css_class,
            **kwargs
        )

    def decompress(self, value):
        if value:
            return value

        return [None, None]


class Html5DateInput(DateInput):
    """Renders an HTML5 date widget."""
    input_type = 'date'

    def __init__(self, date_format='%Y-%m-%d', *args, **kwargs):
        super(Html5DateInput, self).__init__(*args, **kwargs)
        self.date_format = date_format

    def _format_value(self, value):
        value = super(Html5DateInput, self)._format_value(value)

        if self.date_format and isinstance(value, (date, datetime)):
            return value.strftime(self.date_format)

        return value


class Html5DateTimeInput(DateTimeInput):
    """Renders an HTML5 datetime widget."""
    input_type = 'datetime'

    def __init__(self, date_format='%Y-%m-%d %H:%M:%S', *args, **kwargs):
        super(Html5DateTimeInput, self).__init__(date_format=date_format,
                                                 *args,
                                                 **kwargs)


class ReadonlyWidget(TextInput):
    """This renders a readonly field that can also override the default display
    value.
    """
    def render(self, name, value, attrs=None):
        if 'readonly' not in self.attrs:
            # Make sure the field renders as readonly
            self.attrs['readonly'] = 'readonly'

        if 'value' in self.attrs:
            # Override the display value
            value = self.attrs.get('value')

        return super(ReadonlyWidget, self).render(name, value, attrs=attrs)


class CommaSeparatedListWidget(TextInput):
    """Widget for rendering a comma separated list using a text field."""

    def __init__(self, *args, **kwargs):
        super(CommaSeparatedListWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple)):
            # It's a list, join the values for display
            value = ', '.join(map(str, value))

        return super(CommaSeparatedListWidget, self).render(name=name,
                                                            value=value,
                                                            attrs=attrs)

    def value_from_datadict(self, data, files, name, **kwargs):
        value = super(CommaSeparatedListWidget,
                      self).value_from_datadict(data=data, files=files,
                                                name=name, **kwargs)

        if value and isinstance(value, string_types):
            return [item.strip() for item in value.split(',') if item.strip()]

        return value
