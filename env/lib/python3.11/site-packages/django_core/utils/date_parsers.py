from __future__ import unicode_literals

import datetime

from dateutil.parser import parse
from django.utils.six import string_types
from django.utils.timezone import pytz


def now_by_tz(tz='US/Central', ignoretz=True):
    """Gets the current datetime object by timezone.

    :param tz: is the timezone to get the date for.  tz can be passed as a
        string or as a timezone object. (i.e. 'US/Central' or
        pytz.timezone('US/Central'), etc)
    :param ignoretz: will ignore the timezone portion of the datetime object and
        tzinfo will be None.
    :return: the current datetime object by tz

    Examples:

    >>> now_by_tz('US/Pacific')
    2011-09-28 10:06:01.130025
    >>> now_by_tz('US/Pacific', False)
    2011-09-28 10:06:01.130025-07:00
    >>> now_by_tz(pytz.timezone('US/Central'))
    2011-09-28 12:06:01.130025
    >>> now_by_tz(pytz.timezone('US/Central'), False)
    2011-09-28 12:06:01.130025-05:00

    """
    if isinstance(tz, string_types):
        tz = pytz.timezone(tz)

    if ignoretz:
        return datetime.datetime.now(tz).replace(tzinfo=None)
    return datetime.datetime.now(tz)


def tz_to_utc(dt, tz, ignoretz=True):
    """Converts a datetime object from the specified timezone to a UTC datetime.

    :param tz: the timezone the datetime is currently in.  tz can be passed
        as a string or as a timezone object. (i.e. 'US/Central' or
        pytz.timezone('US/Central'), etc)
    :param ignoretz: will ignore the timezone portion of the datetime object and
        tzinfo will be None.
    :return: the datetime object by in UTC time.

    Examples:

    >>> tz_to_utc(datetime.datetime(2011, 11, 25, 9), 'US/Central')
    2011-11-25 15:00:00
    >>> tz_to_utc(datetime.datetime(2011, 11, 25, 9), pytz.timezone('US/Central'))
    2011-11-25 15:00:00
    >>> tz_to_utc(datetime.datetime(2011, 11, 25, 9), 'US/Central', False)
    2011-11-25 15:00:00+00:00

    """
    if isinstance(tz, string_types):
        tz = pytz.timezone(tz)

    dt = tz.localize(dt)
    dt = datetime.datetime.astimezone(dt, pytz.timezone('UTC'))

    if ignoretz:
        return dt.replace(tzinfo=None)
    return dt


def utc_to_tz(dt, tz, ignoretz=True):
    """ Converts UTC datetime object to the specific timezone.

    :param dt: the UTC datetime object to convert.
    :param tz: the timezone to convert the UTC datetime object info.  tz can be
               passed as a string or as a timezone object. (i.e. 'US/Central' or
               pytz.timezone('US/Central'), etc)
    :param ignoretz: will ignore the timezone portion of the datetime object and
                     tzinfo will be None.
    :return: the datetime object by in UTC time.

    Examples:

    >>> utc_to_tz(datetime.datetime(2011, 11, 25, 9), pytz.timezone('US/Central'))
    2011-11-25 03:00:00
    >>> utc_to_tz(datetime.datetime(2011, 11, 25, 9), 'US/Central', False)
    2011-11-25 03:00:00-06:00

    """
    if isinstance(tz, string_types):
        tz = pytz.timezone(tz)

    dt = pytz.utc.localize(dt)
    dt = dt.astimezone(tz)

    if ignoretz:
        return dt.replace(tzinfo=None)
    return dt


def parse_date(dt, ignoretz=True, as_tz=None):
    """
    :param dt: string datetime to convert into datetime object.
    :return: date object if the string can be parsed into a date. Otherwise,
        return None.

    :see: http://labix.org/python-dateutil

    Examples:

    >>> parse_date('2011-12-30')
    2011-12-30
    >>> parse_date('12/30/2011')
    2011-12-30

    """
    dttm = parse_datetime(dt, ignoretz=ignoretz)
    return None if dttm is None else dttm.date()


def parse_datetime(dt, ignoretz=True, **kwargs):
    """
    :param dt: string datetime to convert into datetime object.
    :return: datetime object if the string can be parsed into a datetime.
        Otherwise, return None.

    :see: http://labix.org/python-dateutil

    Examples:

    >>> parse_datetime('2011-12-30 13:45:12 CDT')
    2011-12-30 13:45:12
    >>> parse_datetime('12/30/2011 13:45:12 CDT')
    2011-12-30 13:45:12
    >>> parse_datetime('2011-12-30 13:45:12 CDT', ignoretz=False)
    2011-12-30 13:45:12-06:00
    >>> parse_datetime('12/30/2011 13:45:12 CDT', ignoretz=False)
    2011-12-30 13:45:12-06:00

    """
    try:
        return parse(dt, ignoretz=ignoretz, **kwargs)
    except:
        return None


"""
print(parse_date('2011-12-30'))
print(parse_date('12/30/2011'))
print(parse_datetime('hello world'))
print(parse_datetime('12/30/2011 13:45:12 CDT'))
print(parse_datetime('2011-12-30 13:45:12 CDT', ignoretz=False))
print(parse_datetime('12/30/2011 13:45:12 CDT', ignoretz=False))
print(utc_to_tz(datetime.datetime(2011, 11, 25, 9), pytz.timezone('US/Central')))
print(utc_to_tz(datetime.datetime(2011, 11, 25, 9), 'US/Central', False))
print(tz_to_utc(datetime.datetime(2011, 11, 25, 9), pytz.timezone('US/Central')))
print(tz_to_utc(datetime.datetime(2011, 11, 25, 9), 'US/Central', False))
print(now_by_tz('US/Pacific'))
print(now_by_tz('US/Pacific', False))
print(now_by_tz(pytz.timezone('US/Central')))
print(now_by_tz(pytz.timezone('US/Central'), False))
"""