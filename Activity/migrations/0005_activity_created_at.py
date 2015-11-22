# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0004_activityjoin_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 21, 14, 42, 42, 79569, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
