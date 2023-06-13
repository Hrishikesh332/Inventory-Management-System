from __future__ import unicode_literals

from datetime import datetime

from .db.models.managers import CommonManager
from .db.models.managers import TokenManager


class TokenAuthorizationManager(TokenManager, CommonManager):
    """Model manager for token authorizations."""

    def expire_by_email(self, email_address, **kwargs):
        """Expires tokens for an email address or email addresses.

        :param email_address: the string email address or emails addresses to
            expire tokens for.
        :param reason: the codified reason for the tokens.  If explicitly set
            to None, this will expire all tokens for the email provided.
        """
        if not email_address:
            # no email(s) provided.  Nothing to do.
            return None

        if isinstance(email_address, (set, list, tuple)):
            email_address = [e.strip() for e in set(email_address)
                             if e and e.strip()]

            # make sure there's at least 1 valid email address
            if len(email_address) <= 0:
                # no valid emails
                return None

            kwargs['email_address__in'] = email_address
        else:
            kwargs['email_address'] = email_address

        # try setting the reason default if one exists (in the case of proxy
        # models)
        if 'reason' not in kwargs and self.model.reason_default:
            kwargs['reason'] = self.model.reason_default

        if 'reason' in kwargs and kwargs.get('reason') is None:
            # explicitly setting the reason to None will expire all tokens for
            # a user regardless of the reason.
            del kwargs['reason']

        self.filter(**kwargs).update(expires=datetime(1970, 1, 1))

    def expire_by_emails(self, email_addresses, **kwargs):
        """Expires tokens by a list of email addresses."""
        self.expire_by_email(email_address=email_addresses, **kwargs)
