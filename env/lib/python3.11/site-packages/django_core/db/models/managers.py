from __future__ import unicode_literals

import math

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http.response import Http404
from django.template.defaultfilters import slugify
from django_core.utils.random_utils import random_alphanum


class BaseManager(models.Manager):

    def get_or_none(self, prefetch_related=None, select_related=False,
                    **kwargs):
        """Gets a single object based on kwargs or None if one is not found.

        :param prefetch_related: list or tuple of fields to prefetch for an
            object.  This takes precedence over select_related.

            Example:

            >> get_or_none(prefetch_related=['some_field',
            ...                              'some_field__some_fields_field'])

            See:
            https://docs.djangoproject.com/en/dev/ref/models/querysets/#prefetch-related

        :param select_related: boolean when set to True will follow foreign-key
            relationships to prevent many db queries when looping over foreign
            keys. If this value is boolean True, the immediate foreign keys
            will be selected, but not foreign keys of foreign keys.  If this
            value is set to a list or tuple, then those will be the fields to
            to follow and select.

            Example:

            >> # Both of the following are valid
            >> get_or_none(select_related=True)
            >> get_or_none(select_related=['some_field',
            ...                            'some_field__some_fields_field'])

            See: https://docs.djangoproject.com/en/dev/ref/models/querysets/
        :param kwargs: list of fields and their values to retrieve.

        """
        try:
            if prefetch_related:
                query_set = self.prefetch_related(*prefetch_related)
            elif select_related == True:
                query_set = self.select_related()
            elif isinstance(select_related, (list, tuple)):
                query_set = self.select_related(*select_related)
            else:
                query_set = self

            return query_set.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CommonManager(BaseManager):

    def get_by_id(self, id, **kwargs):
        """Gets a document by an id.

        :param id: id of the document to retrieve.
        """
        return self.get_or_none(id=id, **kwargs)

    def get_by_id_or_404(self, id, **kwargs):
        """Gets by a instance instance r raises a 404 is one isn't found."""
        obj = self.get_by_id(id=id, **kwargs)

        if obj:
            return obj

        raise Http404

    def get_by_ids(self, ids, **kwargs):
        """Gets documents by ids.

        :param ids: list of ids of documents to return
        :param fields: a tuple of field names to return.  If None, all fields
            are returned (default).
        """
        return self.filter(id__in=ids)

    def bulk_create(self, objs, *args, **kwargs):
        """Insert many object at once."""
        if hasattr(self.model, 'save_prep'):
            # Method from AbstractBaseModel. If the model class doesn't
            # subclass AbstractBaseModel, then don't call this.
            self.model.save_prep(instance_or_instances=objs)

        return super(CommonManager, self).bulk_create(objs=objs,
                                                      *args,
                                                      **kwargs)

    def delete_by_id(self, id):
        """Deletes a document by id."""
        return self.delete_by_ids(ids=[id])

    def delete_by_ids(self, ids):
        """Delete objects by ids.

        :param ids: list of objects ids to delete.
        :return: True if objects were deleted.  Otherwise, return False if no
                objects were found or the delete was not successful.
        """
        try:
            self.filter(id__in=ids).delete()
            return True
        except self.model.DoesNotExist:
            return False


class SlugManager(BaseManager):
    """Manager mixin for slugs."""

    def get_by_slug(self, slug, **kwargs):
        try:
            return self.get(slug=slug, **kwargs)
        except self.model.DoesNotExist:
            return None

    def get_by_slug_or_404(self, slug, **kwargs):
        group = self.get_by_slug(slug, **kwargs)

        if group:
            return group

        raise Http404

    def is_slug_available(self, slug, **kwargs):
        """Checks to see if a slug is available. If the slug is already being used
        this method returns False.  Otherwise, return True.
        """
        try:
            self.get(slug=slug, **kwargs)
            return False
        except self.model.DoesNotExist:
            return True

    def get_next_slug(self, slug, **kwargs):
        """Gets the next available slug.

        :param slug: the slug to slugify
        :param kwargs: additional filter criteria to check for when looking for
            a unique slug.

        Example:

        if the value "my-slug" is already taken, this method will append "-n"
        to the end of the slug until the next available slug is found.

        """
        original_slug = slug = slugify(slug)
        count = 0

        while not self.is_slug_available(slug=slug, **kwargs):
            count += 1
            slug = '{0}-{1}'.format(original_slug, count)

        return slug


class TokenManager(BaseManager):
    """Manager Mixin for tokens."""

    def get_by_token(self, token, **kwargs):
        """Get by token."""
        return self.get_or_none(token=token, **kwargs)

    def get_by_token_or_404(self, token, **kwargs):
        group = self.get_by_token(token, **kwargs)

        if group:
            return group

        raise Http404

    def get_next_token(self, length=15, **kwargs):
        """Gets the next available token.

        :param length: length of the token
        :param kwargs: additional filter criteria to check for when looking for
            a unique token.

        """
        return self.get_available_tokens(count=1,
                                         token_length=length,
                                         **kwargs)[0]

    def get_available_tokens(self, count=10, token_length=15, **kwargs):
        """Gets a list of available tokens.

        :param count: the number of tokens to return.
        :param token_length: the length of the tokens.  The higher the number
            the easier it will be to return a list.  If token_length == 1
            there's a strong probability that the enough tokens will exist in
            the db.

        """
        # This is the number of extra tokens to try and retrieve so calls to
        # the db can be limited
        token_buffer = int(math.ceil(count * .05))

        if token_buffer < 5:
            token_buffer = 5

        available = set([])

        while True:
            tokens = [random_alphanum(length=token_length)
                      for t in range(count + token_buffer)]
            db_tokens = self.filter(token__in=tokens).values_list('token',
                                                                  flat=True)
            available.update(set(tokens).difference(db_tokens))

            if len(available) >= count:
                return list(available)[:count]


class UserManager(models.Manager):
    """Manager Mixin for models that have a user."""

    def get_by_user(self, user, **kwargs):
        return self.get_by_user_id(user_id=user.id, **kwargs)

    def get_by_user_id(self, user_id, **kwargs):
        try:
            return self.filter(user_id=user_id)
        except self.model.DoesNotExist:
            return []


class GenericManager(models.Manager):

    def get_or_create_generic(self, content_object, **kwargs):
        """Gets or creates a generic object.  This is a wrapper for
        get_or_create(...) when you need to get or create a generic object.

        :param obj: the object to get or create
        :param kwargs: any other kwargs that the model accepts.
        """
        content_type = ContentType.objects.get_for_model(content_object)
        return self.get_or_create(content_type=content_type,
                                  object_id=content_object.id,
                                  **kwargs)

    def get_by_content_type(self, content_type):
        """Gets all objects by a content type."""
        return self.filter(content_type=content_type)

    def get_by_model(self, model):
        """Gets all object by a specific model."""
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content_type=content_type)
