from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.utils.decorators import method_decorator
from django_core.views.mixins.common import CommonSingleObjectViewMixin


class CreatorRequiredViewMixin(CommonSingleObjectViewMixin):
    """Mixin that requires the self.object be created by the authenticated
    user.
    """
    def dispatch(self, request, *args, **kwargs):
        # does self.object exist at this point?
        obj = self.get_creator_required_object()

        if not obj:
            raise Http404

        if obj.created_user_id != request.user.id:
            raise PermissionDenied

        return super(CreatorRequiredViewMixin, self).dispatch(request,
                                                              *args,
                                                              **kwargs)

    def get_creator_required_object(self):
        return self.get_object()


class LoginRequiredViewMixin(object):
    """Use this with CBVs to ensure user is logged in."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredViewMixin, self).dispatch(*args, **kwargs)


class StaffRequiredViewMixin(LoginRequiredViewMixin):
    """Require a logged in Staff member."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        return super(StaffRequiredViewMixin, self).dispatch(request,
                                                            *args,
                                                            **kwargs)


class SuperuserRequiredViewMixin(LoginRequiredViewMixin):
    """Require a logged in user to be a superuser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        return super(SuperuserRequiredViewMixin, self).dispatch(request,
                                                                *args,
                                                                **kwargs)
