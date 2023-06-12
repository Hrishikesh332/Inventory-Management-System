from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django_core.utils.validators import is_valid_email


class EmailOrUsernameBackend(ModelBackend):
    """Authentication backend to allow a user to login via email address or
    username.
    """

    def authenticate(self, username, password):
        """
        :param username: this is the email or username to check
        """
        # If username is an email address, then try to pull it up
        user = self.get_by_username_or_email(username)

        if not user:
            return None

        if user.check_password(password):
            return user

        return None

    def get_by_username_or_email(self, username_or_email):
        username_or_email = username_or_email.strip().lower()

        if is_valid_email(username_or_email):
            return self.get_by_email(username_or_email)

        return self.get_by_username(username_or_email)

    def get_by_email(self, email):
        User = get_user_model()
        try:
            return User.objects.get(email=email.lower())
        except User.DoesNotExist:
            return None

    def get_by_username(self, username):
        User = get_user_model()
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
