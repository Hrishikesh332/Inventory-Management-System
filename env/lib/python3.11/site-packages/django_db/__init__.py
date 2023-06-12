import os
from uuid import uuid4

import pymysql
import django
from django.db import connections, close_old_connections

from . import settings

# replace mysqldb with pymysql
pymysql.install_as_MySQLdb()

# set os env django settings and django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.__name__)
django.setup()


class Router(object):
    app_label = ''

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == self.app_label:
            return db == self.app_label
        return None


def add_db(db_conf):
    app_label = 'al_' + str(uuid4())

    settings.DATABASES[app_label] = db_conf

    router_class_name = 'Router' + app_label.capitalize()
    setattr(
        settings,
        router_class_name,
        type(router_class_name, (Router,), dict(app_label=app_label)),
    )
    settings.DATABASE_ROUTERS.append(
        '.'.join([settings.__name__, router_class_name])
    )
    connections.close_all()
    return app_label


def create_model(model):
    with connections[model._meta.app_label].schema_editor() as schema_editor:
        schema_editor.create_model(model)


def delete_model(model):
    with connections[model._meta.app_label].schema_editor() as schema_editor:
        schema_editor.delete_model(model)


def check_table_exists(model):
    conn = connections[model._meta.app_label]
    cursor = conn.cursor()
    table_names = [table_info.name for table_info in conn.introspection.get_table_list(cursor)]
    cursor.close()
    connections.close_all()
    return model._meta.db_table in table_names


def sync_table(model):
    if not check_table_exists(model):
        create_model(model)
