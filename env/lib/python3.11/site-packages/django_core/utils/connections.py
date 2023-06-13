from __future__ import unicode_literals

from urllib.error import URLError

from django_core.utils.loading import get_setting


try:
    # python 3
    from urllib.request import urlopen
except ImportError:
    # python 2
    from urllib import urlopen


# this is the url to check
INTERNET_CONNECTION_URL = get_setting(key='INTERNET_CONNECTION_URL',
                                      default='http://google.com')


def has_internet_connection(url=INTERNET_CONNECTION_URL):
    """Returns a boolean indicating if an internet connection if present.

    :param url: the url used to check if a connection can be made
    """
    try:
        urlopen(url=url)
        return True
    except URLError:
        return False
