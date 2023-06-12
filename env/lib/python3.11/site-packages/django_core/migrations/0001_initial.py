# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('token', models.CharField(unique=True, max_length=100, db_index=True)),
                ('created_dttm', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('last_modified_dttm', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('email_address', models.EmailField(blank=True, null=True, max_length=254)),
                ('expires', models.DateTimeField()),
                ('reason', models.CharField(blank=True, null=True, max_length=50)),
                ('created_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='django_core_tokenauthorization_created_user+')),
                ('last_modified_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='django_core_tokenauthorization_last_modified_user+')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='django_core_tokenauthorization_user+')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
