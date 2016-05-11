# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_auto_20160508_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='value',
            field=models.IntegerField(default=0, verbose_name='\u62e5\u6709\u7684\u8dd1\u8f66\u7684\u4ef7\u503c'),
        ),
    ]
