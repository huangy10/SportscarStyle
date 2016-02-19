# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0011_auto_20160217_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='closed',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x8a\xa5\xe5\x90\x8d\xe6\x98\xaf\xe5\x90\xa6\xe5\x85\xb3\xe9\x97\xad'),
        ),
        migrations.AddField(
            model_name='activity',
            name='closed_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 19, 14, 11, 7, 415939, tzinfo=utc), verbose_name=b'\xe5\x85\xb3\xe9\x97\xad\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
