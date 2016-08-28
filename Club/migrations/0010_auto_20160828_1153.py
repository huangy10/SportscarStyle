# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0009_auto_20160821_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='identified',
            field=models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8ba4\u8bc1'),
        ),
        migrations.AlterField(
            model_name='club',
            name='identified_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u8ba4\u8bc1\u65e5\u671f'),
        ),
    ]
