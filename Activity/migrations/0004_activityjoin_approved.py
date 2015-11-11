# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0003_activity_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityjoin',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
