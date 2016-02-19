# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0012_auto_20160219_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='closed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x85\xb3\xe9\x97\xad\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
