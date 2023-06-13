# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_core', '0002_auto_20150504_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenauthorization',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tokenauthorization',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
