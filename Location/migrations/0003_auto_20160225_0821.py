# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Location', '0002_auto_20151110_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertracking',
            name='location_available',
            field=models.BooleanField(default=False, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80\xe6\x95\xb0\xe6\x8d\xae\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaf\xe7\x94\xa8'),
        ),
        migrations.AddField(
            model_name='usertracking',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 25, 8, 21, 19, 625717, tzinfo=utc), verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usertracking',
            name='user',
            field=models.ForeignKey(related_name='location', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]
