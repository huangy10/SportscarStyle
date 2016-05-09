# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereddevices',
            name='device_type',
            field=models.CharField(default=b'ios', max_length=50),
        ),
    ]
