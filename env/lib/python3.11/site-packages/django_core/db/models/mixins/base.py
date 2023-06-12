from __future__ import unicode_literals

from copy import deepcopy
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_core.db.models.managers import CommonManager
from django_core.utils.list_utils import make_obj_list


@python_2_unicode_compatible
class AbstractBaseModel(models.Model):
    """Base model for other db model to extend.  This class contains common
    model attributes needed by almost all models.

    Fields:

    * created: created user.  The user who created this instance.
    * created_dttm: created datetime.
    * last_modified: last user to modify this instance
    * last_modified_dttm: updated datetime. Datetime this document was last
        updated.
    """
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_created_user+')
    created_dttm = models.DateTimeField(default=datetime.utcnow)
    last_modified_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_last_modified_user+')
    last_modified_dttm = models.DateTimeField(default=datetime.utcnow)
    objects = CommonManager()

    class Meta:
        abstract = True
        # Default ordering is by id instead of created_dttm for 2 reasons:
        # 1) id is indexed (primary key)
        # 2) it's safer than created_dttm since created_dttm could be the same
        #    value which would lead to inconsistent ording in responses from
        #    queries.  This works because id is an integer field that's auto
        #    incremented.
        ordering = ('-id',)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """Optional kwargs:

        * id_length: the length of characters to use for the id.  Default
            is 10.
        """
        self.__class__.save_prep(self)
        return super(AbstractBaseModel, self).save(*args, **kwargs)

    def get_verbose_name(self):
        """Gets the verbose name for an object."""
        return self._meta.verbose_name

    @classmethod
    def save_prep(cls, instance_or_instances):
        """Common save functionality for all models. This can be called with a
        saved or unsaved instance or one or many objects. This is beneficial
        when additional process needs to happen before a bulk_create which
        doesn't explicitly call the .save on each instance being saved. This
        method will go through each object and do necessary presave processing.

        This method can be extended by classes and implement this abstact class
        by simply creating the def save_prep method and making sure to call
        super class method making sure the save_prep method is properly called
        from each inheriting class:

        All models.CharField will be stripped prior to saving.

        Example:

            @classmethod
            def save_prep(cls, instance_or_instances):
                # Do additional processing for inheriting class
                super(MyInheritingClass, cls).save_prep(instance_or_instances)

        Note: Make sure not to call the save_prep method in the save method of
        inheriting classes or it will get called twice which likely isn't
        wanted since this Abstract class explicitly calls the save_prep on
        save().

        All objects are assumed to have the following fields:

        * id
        * created
        * created_dttm
        * last_modified
        * last_modified_dttm

        """
        instances = make_obj_list(instance_or_instances)

        utc_now = datetime.utcnow()
        for instance in instances:
            instance.last_modified_dttm = utc_now

            if not instance.created_dttm:
                instance.created_dttm = utc_now

            if instance.created_user:
                if not hasattr(instance, 'last_modified') or \
                   not instance.last_modified:
                    instance.last_modified_user = instance.created_user

            instance.strip_fields()

    def strip_fields(self):
        """Strips whitespace from all text related model fields. This includes
        CharField and TextFields and all subclasses of those two fields.
        """
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value and hasattr(value, 'strip'):
                    setattr(self, field.name, value.strip())

    def copy(self, exclude_fields=None, **override_fields):
        """Returns an unsaved copy of this object with all fields except for
        any fields that are unique in the DB. Those fields must be explicitly
        set before saving the instance:

        * id
        * created_dttm
        * last_modified_dttm

        NOTE: If a field doesn't except null values, you must explicitly set
        the value in the override fields or this method will error out since
        you can't set that fields to be null.

        :param exclude_fields: fields to exclude from the copy.  They will
            fallback to the field default if one is given or None.
        :param override_fields: kwargs with fields to override.  The key is the
            field name, the value is the value to set the copied object to.

            Example:

            >> new_obj = some_obj.copy(my_field='hello world')
            >> new_obj.my_field
            'hello world'

        """
        if not exclude_fields:
            exclude_fields = []

        exclude_fields += ['created_dttm', 'last_modified_dttm']
        # Don't copy data for any unique fields.  These must be explicitly set.
        exclude_fields += [field.name
                           for field in self._meta.fields if field.unique]
        instance = deepcopy(self)
        instance.last_modified_user = instance.created_user
        instance.last_modified_user_id = instance.created_user_id

        # unset all the attributes that you don't want copied over
        for field in set(exclude_fields):
            meta = self.__class__._meta
            default = meta.get_field_by_name(field)[0].get_default()
            setattr(instance, field, default or None)

        if override_fields:
            for field, val in override_fields.items():
                setattr(instance, field, val)

        return instance

    @classmethod
    def _get_many_to_many_model(cls, field_name):
        """Get the model for the many to many field.

        :param field_name: field name to get the model for.
        """

        for field in cls._meta.many_to_many:
            if field.attname == field_name:
                if hasattr(field.related, 'parent_model'):
                    # django < 1.8
                    return field.related.parent_model
                return field.related.model

    @classmethod
    def post_save(cls, *args, **kwargs):
        """Adding a hook here so it's safe to call the super's post_save."""
        pass

    @classmethod
    def post_delete(cls, *args, **kwargs):
        """Adding a hook here so it's safe to call the super's post_delete."""
        pass

    @classmethod
    def m2m_changed(cls, *args, **kwargs):
        """Adding a hook here so it's safe to call the super's m2m_changed."""
        pass
