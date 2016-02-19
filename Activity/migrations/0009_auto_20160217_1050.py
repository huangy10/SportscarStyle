# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0008_auto_20160216_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityjoin',
            name='activity',
            field=models.ForeignKey(related_name='applications', to='Activity.Activity'),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='user',
            field=models.ForeignKey(related_name='applied_acts', to=settings.AUTH_USER_MODEL),
        ),
    ]
