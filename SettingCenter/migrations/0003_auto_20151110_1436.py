# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('SettingCenter', '0002_auto_20151108_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingcenter',
            name='blacklist',
            field=models.ManyToManyField(related_name='backlist_ed', to=settings.AUTH_USER_MODEL),
        ),
    ]
