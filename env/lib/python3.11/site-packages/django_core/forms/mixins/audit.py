from django import forms

from .users import UserFormMixin


class AddFormAuditMixin(UserFormMixin, forms.ModelForm):
    """Audit form mixin that ensure created_user and last_modified_user are
    set to the user creating the object.
    """

    def save(self, *args, **kwargs):
        self.instance.created_user = self.user
        self.instance.last_modified_user = self.user
        return super(AddFormAuditMixin, self).save(*args, **kwargs)


class EditFormAuditMixin(UserFormMixin, forms.ModelForm):
    """Audit form mixin that ensure the last_modified_user has been set to the
    user editing the object.
    """

    def save(self, *args, **kwargs):
        self.instance.last_modified_user = self.user
        return super(EditFormAuditMixin, self).save(*args, **kwargs)