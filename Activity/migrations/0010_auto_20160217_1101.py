# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0009_auto_20160217_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='appliers',
            field=models.ManyToManyField(related_name='applied_acts', verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe8\x80\x85', through='Activity.ActivityJoin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='activity',
            field=models.ForeignKey(to='Activity.Activity'),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
