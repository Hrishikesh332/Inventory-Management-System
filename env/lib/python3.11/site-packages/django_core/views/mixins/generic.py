from django.contrib.contenttypes.models import ContentType
from django.http.response import Http404


class GenericObjectViewMixin(object):
    """View mixin that takes the content_type_id and object_id from the url
    and it gets the object it refers to.
    """
    generic_object_content_type = None
    content_object = None

    def dispatch(self, *args, **kwargs):
        try:
            content_type_id = kwargs['content_type_id']
            object_id = kwargs['object_id']
        except:
            raise Http404

        try:
            self.generic_object_content_type = ContentType.objects.get_for_id(
                id=content_type_id
            )
        except:
            raise Http404

        content_model = self.generic_object_content_type.model_class()

        try:
            self.content_object = content_model.objects.get(id=object_id)
        except:
            raise Http404

        return super(GenericObjectViewMixin, self).dispatch(*args,
                                                                **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GenericObjectViewMixin,
                        self).get_context_data(**kwargs)
        context['generic_object_content_type'] = self.generic_object_content_type
        context['content_object'] = self.content_object

        content_object_url = self.get_content_object_url()

        if content_object_url:
            context['content_object_url'] = content_object_url

        return context

    def get_content_object_url(self):
        """Gets the absolute url for the content object."""
        if (self.content_object and
            hasattr(self.content_object, 'get_absolute_url')):
            return self.content_object.get_absolute_url()

        return None
