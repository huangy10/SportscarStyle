# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_auto_20160710_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='district',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5730\u533a', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='job',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'\xe8\xa1\x8c\xe4\xb8\x9a', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='signature',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u7b7e\u540d', blank=True),
        ),
    ]
