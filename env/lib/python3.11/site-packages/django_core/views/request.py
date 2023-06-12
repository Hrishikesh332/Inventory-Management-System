from __future__ import unicode_literals

from django.views.generic.edit import BaseFormView

from ..views.response import JSONResponseMixin


class ApiFormView(JSONResponseMixin, BaseFormView):
    """Form view for Api's to leverage forms and correctly validate query
    string data.
    """

    def get(self, request, *args, **kwargs):

        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form=form)

        return self.form_invalid(form=form)

    def get_form_kwargs(self):
        """Add the 'data' to the form args so you can validate the form
        data on a get request.
        """
        kwargs = super(ApiFormView, self).get_form_kwargs()
        kwargs['data'] = kwargs.get('initial')
        return kwargs

    def form_invalid(self, form, context=None, **kwargs):
        """This will return the request with form errors as well as any
        additional context.
        """
        if not context:
            context = {}

        context['errors'] = form.errors
        return super(ApiFormView, self).render_to_response(context=context,
                                                           status=400)
