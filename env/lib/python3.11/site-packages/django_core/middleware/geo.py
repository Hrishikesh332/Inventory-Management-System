from __future__ import unicode_literals

from django.utils import timezone
from django.utils.timezone import pytz


class TimezoneMiddleware(object):
    """Middleware to get a users timezone if one exists.  That way datetime can
    always be displayed according to either the users preferred setting or
    the browser's setting.

    @see: https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#selecting-the-current-time-zone
    """
    def process_request(self, request):
        tz = request.session.get('user_timezone')

        if tz:
            try:
                timezone.activate(pytz.timezone(tz))
            except:
                timezone.deactivate()
        else:
            timezone.deactivate()

        # Add datetime info the the request. So date/time can be put in context
        # of the user.
        # user_datetime = localtime(datetime.utcnow().replace(tzinfo=utc))
        # request.user_date = user_datetime.date()
        # request.user_datetime = user_datetime
