from __future__ import unicode_literals

import importlib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _

from django.apps import apps


def get_setting(key, **kwargs):
    """Gets a settings key or raises an improperly configured error.

    :param key: the settings key to get.
    :param default: the default value to return if no value is found
    """
    has_default = 'default' in kwargs
    default_val = kwargs.get('default')

    try:
        if has_default:
            return getattr(settings, key, default_val)
        else:
            return getattr(settings, key)
    except Exception as e:
        raise ImproperlyConfigured(
            _('"{0}" setting has not been properly set. {1}').format(key, e)
        )


def get_class_from_settings(settings_key):
    """Gets a class from a setting key.  This will first check loaded models,
    then look in installed apps, then fallback to import from lib.

    :param settings_key: the key defined in settings to the value for
    """
    cls_path = getattr(settings, settings_key, None)
    if not cls_path:
        raise NotImplementedError()

    try:
        # First check to see if it's an installed model
        return get_model_from_settings(settings_key=settings_key)
    except:
        try:
            # Next, check from installed apps
            return get_class_from_settings_from_apps(settings_key=settings_key)
        except:
            # Last, try to load from the full path
            return get_class_from_settings_full_path(settings_key)


def get_model_from_settings(settings_key):
    """Return the django model from a settings key.

    This is the same pattern user for django's "get_user_model()" method. To
    allow you to set the model instance to a different model subclass.

    :param settings_key: the key defined in settings to the value for

    """
    cls_path = getattr(settings, settings_key, None)
    if not cls_path:
        raise NotImplementedError()

    try:
        app_label, model_name = cls_path.split('.')
    except ValueError:
        raise ImproperlyConfigured("{0} must be of the form "
                                   "'app_label.model_name'".format(settings_key))

    model = apps.get_model(app_label, model_name)

    if model is None:
        raise ImproperlyConfigured("{0} refers to model '%s' that has not "
                                   "been installed".format(settings_key))

    return model


def get_class_from_settings_from_apps(settings_key):
    """Try and get a class from a settings path by lookin in installed apps.
    """
    cls_path = getattr(settings, settings_key, None)

    if not cls_path:
        raise NotImplementedError()

    try:
        app_label = cls_path.split('.')[-2]
        model_name = cls_path.split('.')[-1]
    except ValueError:
        raise ImproperlyConfigured("{0} must be of the form "
                                   "'app_label.model_name'".format(
                                                                settings_key))

    app = apps.get_app_config(app_label).models_module

    if not app:
        raise ImproperlyConfigured("{0} setting refers to an app that has not "
                                   "been installed".format(settings_key))

    return getattr(app, model_name)


def get_class_from_settings_full_path(settings_key):
    """Get a class from it's full path.

    Example:

    some.path.module.MyClass
    """
    cls_path = getattr(settings, settings_key, None)

    if not cls_path:
        raise NotImplementedError()

    try:
        module_name, class_name = cls_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("{0} must be of the form "
                                   "'some.path.module.MyClass'".format(
                                                                settings_key))

    manager_module = importlib.import_module(module_name)

    if not manager_module:
        raise ImproperlyConfigured("{0} refers to a module that has not been "
                                   "installed".format(settings_key))

    return getattr(manager_module, class_name)


def get_function_from_settings(settings_key):
    """Gets a function from the string path defined in a settings file.

    Example:

    # my_app/my_file.py
    def some_function():
        # do something
        pass

    # settings.py
    SOME_FUNCTION = 'my_app.my_file.some_function'

    > get_function_from_settings('SOME_FUNCTION')
    <function my_app.my_file.some_function>
    """

    renderer_func_str = getattr(settings, settings_key, None)
    if not renderer_func_str:
        return None

    module_str, renderer_func_name = renderer_func_str.rsplit('.', 1)

    try:
        mod = importlib.import_module(module_str)
        return getattr(mod, renderer_func_name)
    except Exception:
        return None
