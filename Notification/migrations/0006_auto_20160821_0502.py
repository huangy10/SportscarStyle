# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0005_auto_20160821_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message_type_backup',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
