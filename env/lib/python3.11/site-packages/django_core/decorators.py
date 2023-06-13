from __future__ import unicode_literals

from django.conf import settings


def turn_emails_off(view_func):
    """Turns emails off so no emails will be sent."""

    # Dummy email backend so no emails are sent.
    EMAIL_BACKEND_DUMMY = 'django.core.mail.backends.dummy.EmailBackend'

    def decorated(request, *args, **kwargs):
        orig_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = EMAIL_BACKEND_DUMMY

        response = view_func(request, *args, **kwargs)
        settings.EMAIL_BACKEND = orig_email_backend
        return response

    return decorated
