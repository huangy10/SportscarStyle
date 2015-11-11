# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('SettingCenter', '0003_auto_20151110_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingcenter',
            name='blacklist',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
