# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0006_auto_20160821_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='checked',
            field=custom.fields.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe6\x93\x8d\xe4\xbd\x9c'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='flag',
            field=custom.fields.BooleanField(default=False, verbose_name=b'\xe4\xbf\x9d\xe7\x95\x99\xe5\xad\x97\xe6\xae\xb5'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=custom.fields.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe8\xaf\xbb'),
        ),
        migrations.AlterField(
            model_name='registereddevices',
            name='is_active',
            field=custom.fields.BooleanField(default=True),
        ),
    ]
