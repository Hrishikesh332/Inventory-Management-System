from __future__ import unicode_literals

from django import forms


class PagingFormMixin(forms.Form):
    """Form mixin that includes paging page number and page size."""
    p = forms.IntegerField(label='Page', initial=1, required=False)
    ps = forms.IntegerField(label='Page Size', initial=25, required=False)
