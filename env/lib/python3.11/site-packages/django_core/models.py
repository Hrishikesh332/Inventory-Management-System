from __future__ import unicode_literals

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .managers import TokenAuthorizationManager
from .db.models.mixins.base import AbstractBaseModel
from .db.models.mixins.tokens import AbstractTokenModel


@python_2_unicode_compatible
class TokenAuthorization(AbstractTokenModel, AbstractBaseModel):
    """Model that provides a token for authorization purposes.

    Fields:

    * email_address: any email address needed for the specific authorization
        purposes.  For example, if it's the 'CHANGE_EMAIL' flow, this would be
        the new email address.
    * expires: the date and time when the token expires
    * reason: the codified reason the token was generated.  This is preferably
        a constant but can be any string value.
    * user: a foreign key to the user model. This can be any user needed for
        the specific authorization purpose. For example, if this was an
        "invite to join a system" flow, once the user created their account, the
        user object can be placed back on this authorization for traceability
        purposes.
    * text: free text.  This can be anything additional text needed.  For
        example, if this is a invite to join a site token auth then this could
        be a custom message to the invited user.
    * email_sent: boolean indicating if an email has been sent for this token
        authorization.  Useful if you have a workflow where you need to track
        if an email was sent to a user from a background task such as celery.

    All of the below fields can be configured in proxy models to redefine the
    defaults values:

    * default_token_duration_days: the number of days until the token expires.
    * reason_default: the string value for why the token is being created.
    * token_length: the default length of the token
    """
    email_address = models.EmailField(db_index=True, blank=True, null=True)
    expires = models.DateTimeField()
    reason = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_user+',
        blank=True,
        null=True)
    text = models.TextField(blank=True, null=True)
    email_sent = models.BooleanField(default=False)

    default_token_duration_days = 7
    reason_default = None
    token_length = 50
    objects = TokenAuthorizationManager()

    def __str__(self, *args, **kwargs):
        return str(self.id)

    def save(self, *args, **kwargs):

        if not self.expires:
            # token is valid for self.default_token_duration_days
            self.expires = (datetime.utcnow() +
                            timedelta(days=self.default_token_duration_days))

        if not self.id and not self.reason and self.reason_default:
            self.reason = self.reason_default

        super(TokenAuthorization, self).save(*args, **kwargs)

    def is_valid(self):
        """Boolean indicating if the token is valid."""
        return not self.is_expired()

    def is_expired(self):
        """Boolean indicating if the token for the has expired."""
        return datetime.utcnow() > self.expires

    def expire(self, auto_save=True):
        """Expires the change email token so it's no longer valid.

        :param auto_save: boolean indicating if the object should be saved after
            expiring the token.  If True, this will also make a call to the
            "save()" method.  Otherwise, the save will have to be called
            manually.
        """
        self.expires = datetime(1970, 1, 1)

        if auto_save:
            self.save()
