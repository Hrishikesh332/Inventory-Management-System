# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenauthorization',
            name='email_address',
            field=models.EmailField(max_length=254, db_index=True, blank=True, null=True),
        ),
    ]
