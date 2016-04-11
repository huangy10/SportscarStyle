# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0004_auto_20160405_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='checked',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe6\x93\x8d\xe4\xbd\x9c'),
        ),
    ]
