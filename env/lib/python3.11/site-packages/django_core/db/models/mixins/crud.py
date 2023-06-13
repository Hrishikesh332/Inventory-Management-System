from django.db import models

from django_core.exceptions import NotAllowed


class AbstractSafeDeleteModelMixin(models.Model):
    """Give a model safe delete logic so an indicator can be set to is_deleted
    and not removed from the database.
    """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete_safe(self):
        self.is_deleted = True
        self.save()


class ReadOnlyModelMixin(models.Model):
    """This is a wrapper class around a model so all methods and fields
    can be used the same as the extending model, but this doesn't allow the 
    model instance to be saved.
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # This model is read only and doesn't allow saving
        raise NotAllowed(_("Read only models don't allow calling the .save() "
                           "method."))
