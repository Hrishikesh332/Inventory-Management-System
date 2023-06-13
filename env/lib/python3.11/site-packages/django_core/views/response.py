from copy import deepcopy
import json

from django.forms import Form
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_spaces_between_tags
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView


class JSONResponseMixin(object):
    """Mixin For returning a json response."""

    def render_to_response(self, context, **kwargs):
        return self.get_json_response(content=context, **kwargs)

    def get_json_response(self, content, **kwargs):
        """Returns a json response object."""

        # Don't care to return a django form or view in the response here.
        # Remove those from the context.
        if isinstance(content, dict):
            response_content = {k: deepcopy(v) for k, v in content.items()
                                if k not in ('form', 'view') or k in ('form', 'view')
                                and not isinstance(v, (Form, View))}
        else:
            response_content = content

        return HttpResponse(content=json.dumps(response_content),
                            content_type='application/json; charset=utf-8',
                            **kwargs)


class JSONHybridTemplateView(JSONResponseMixin, TemplateView):

    def render_to_response(self, context):

        if self.request.is_ajax():
            return JSONResponseMixin.render_to_response(self, context)

        return TemplateView.render_to_response(self, context)


class JSONHybridProcessFormViewMixin(JSONResponseMixin):
    """Hybrid mixin that handles form processing.

    Fields:

    json_template_name: if provided, this template will be used to render
        an html template response that will be returned in the response data.

    Example:

    class MyView(JSONHybridProcessFormViewMixin, CreateView):
        json_template_name = 'path/to/json_template.html'

        def get_json_context_data(self, **kwargs):
            context = super(MyView, self).get_json_context_data(**kwargs)
            context['my_json_template_var'] = 'hello world'
            return context

    Successful JSON response (form is valid):

    {
        'html': '<div>Some rendererd html response "hello world"</div>'
    }
    """
    json_template_name = None

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            context = {}

            if self.json_template_name:
                json_context = self.get_json_context_data(**{
                    self.get_context_object_name(self.object): self.object
                })
                html = render_to_string(template_name=self.json_template_name,
                                        dictionary=json_context)
                context['html'] = strip_spaces_between_tags(html.strip())
            else:
                context.update(self.get_json_context_data())

            return JSONResponseMixin.render_to_response(self, context=context)

        return super(JSONHybridProcessFormViewMixin, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            context = {'errors': form.errors}
            return JSONResponseMixin.render_to_response(self, context)

        return super(JSONHybridProcessFormViewMixin, self).form_invalid(form)

    def get_json_context_data(self, **kwargs):
        return kwargs or {}


class JSONHybridCreateView(JSONHybridProcessFormViewMixin, CreateView):
    """Hybrid view that handles regular create requests as well as json create
    requests.
    """
    def render_to_response(self, context):

        if self.request.is_ajax():
            return JSONHybridProcessFormViewMixin.render_to_response(self,
                                                                     context)

        return CreateView.render_to_response(self, context)


class JSONHybridUpdateView(JSONHybridProcessFormViewMixin, UpdateView):
    """Hybrid view that handles regular update requests as well as json update
    requests.
    """
    def render_to_response(self, context):

        if self.request.is_ajax():
            return JSONHybridProcessFormViewMixin.render_to_response(self,
                                                                     context)

        return UpdateView.render_to_response(self, context)


class JSONHybridDeleteView(JSONResponseMixin, DeleteView):

    def render_to_response(self, context):

        if self.request.is_ajax():
            return JSONResponseMixin.render_to_response(self, context)

        return DeleteView.render_to_response(self, context)

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if self.request.is_ajax():
            return JSONResponseMixin.render_to_response(self, context={})

        return HttpResponseRedirect(success_url)


class JSONResponse(HttpResponse):
    """Returns a HttpResponse that has content that's json encoded. Returns a
    status of 200.

    Response content sample::

        {
            activity: "activity html",
            additional_content_key1: additional_content_value1
        }

    :param content: a dictionary of content that should be returned with the
        response.
    :return: HttpResponse with json encoded activity content.

    """
    def __init__(self, content, status=200, **kwargs):
        super(JSONResponse, self).__init__(content=json.dumps(content),
                                           content_type='application/json',
                                           status=status,
                                           **kwargs)
