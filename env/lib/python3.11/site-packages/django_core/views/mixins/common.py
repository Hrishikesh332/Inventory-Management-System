from __future__ import unicode_literals


class CommonSingleObjectViewMixin(object):

    def get_object(self, **kwargs):
        """Sometimes preprocessing of a view need to happen before the object
        attribute has been set for a view.  In this case, just return the
        object if it has already been set when it's called down the road since
        there's no need to make another query.
        """
        if hasattr(self, 'object') and self.object:
            return self.object

        obj = super(CommonSingleObjectViewMixin, self).get_object(**kwargs)
        self.object = obj
        return obj
