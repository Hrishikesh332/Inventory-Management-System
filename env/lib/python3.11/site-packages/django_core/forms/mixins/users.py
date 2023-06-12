from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _


class UserFormMixin(object):
    """Form mixin that puts the user on the form object."""

    def __init__(self, user=None, *args, **kwargs):
        if not hasattr(self, 'user'):
            if user is None:
                raise Exception('user is required for this form.')

            self.user = user

        super(UserFormMixin, self).__init__(*args, **kwargs)


class UserAuthorizationRequiredForm(UserFormMixin, forms.Form):
    """Form for requiring a user to enter their password to successfully pass
    form validation.  This is useful for flows like:

    * change_email
    * change_password
    """
    error_messages = {
        'password_incorrect': _('Your old password was entered incorrectly. '
                                'Please enter it again.'),
    }
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )

        return password
