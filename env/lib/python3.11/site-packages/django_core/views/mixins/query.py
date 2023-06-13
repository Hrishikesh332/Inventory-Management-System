from __future__ import unicode_literals


class QueryStringAliasViewMixin(object):
    """Mixin to let you map GET query string keys to form keys.

    This allows you to use alias keys in your forms so you can keeps shorter
    urls or rename params in the GET query string that will map nicely with
    django's forms.

    This only applies to the request's GET method. If a short key is used it
    will be mapped and a new "initial" dict will be returned for the form
    with the correct initial mapping.  If a short key doesn't exist, the key
    will be used as-is.

    Example:

    Consuming view implements the following attribute::

        query_key_mapper = {'t': 'title'}

    and a url query string is::

        ?t=hello&foo=bar

    This will result in an initial dict for the form being returned as::

        {
            'title': 'hello',
            'foo': 'bar'
        }

    """
    query_key_mapper = None

    def dispatch(self, *args, **kwargs):
        self.query_key_mapper = self.get_query_key_mapper()
        return super(QueryStringAliasViewMixin, self).dispatch(*args, **kwargs)

    def map_query_string(self):
        """Maps the GET query string params the the query_key_mapper dict and
        updates the request's GET QueryDict with the mapped keys.
        """
        if (not self.query_key_mapper or
            self.request.method == 'POST'):
            # Nothing to map, don't do anything.
            # return self.request.POST
            return {}

        keys = list(self.query_key_mapper.keys())

        return {self.query_key_mapper.get(k) if k in keys else k: v.strip()
                for k, v in self.request.GET.items()}

    def get_initial(self):
        initial = super(QueryStringAliasViewMixin, self).get_initial()
        initial.update(self.map_query_string())
        return initial

    def get_query_key_mapper(self):
        """Returns a dictionary of the query params trying to be mapped."""
        return self.query_key_mapper if self.query_key_mapper else {}
