# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0002_auto_20160226_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='identified',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81'),
        ),
        migrations.AddField(
            model_name='club',
            name='identified_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
