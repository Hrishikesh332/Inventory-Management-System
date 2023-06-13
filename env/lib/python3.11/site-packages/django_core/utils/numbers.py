


def simple_format(num):
    """Takes a number and returns the simplest format for the number removing
    all trailing 0's and the '.' if it's the trailing character.

    >>> simple_format(123)
    '123'
    >>> simple_format(123.0)
    '123'
    >>> simple_format(123.01100)
    '123.011'
    """
    return ('%f' % num).rstrip('0').rstrip('.')
