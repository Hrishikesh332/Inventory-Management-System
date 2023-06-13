

class DotNotationDict(dict):
    """Dictionary that has the ability to accesses attributes using dot
    notation.  Example:

    >>> x = DotNotationDict({'hello': {'testing':'world'}})
    >>> x.get('hello').get('testing) == x.get_by_dot_notation('hello.testing')

    """
    def get_by_dot_notation(self, dot_notation):
        chain = dot_notation.split('.')
        val = None

        for index, key in enumerate(chain):
            val = self.get(key) if index == 0 else val.get(key)

            if not val:
                return None

            if index == len(chain) - 1:
                return val

        return None
