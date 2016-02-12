# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0013_userrelationsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrelationsetting',
            name='blacklist_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 11, 11, 6, 5, 253117, tzinfo=utc), verbose_name=b'\xe6\x8b\x89\xe9\xbb\x91\xe6\x97\xb6\xe9\x97\xb4'),
            preserve_default=False,
        ),
    ]
