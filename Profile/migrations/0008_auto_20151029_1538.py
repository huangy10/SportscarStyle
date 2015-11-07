# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0007_auto_20151029_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='interest',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u5730\u533a'),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='job',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='job',
            field=models.CharField(default=b'', max_length=64, verbose_name=b'\xe8\xa1\x8c\xe4\xb8\x9a'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='signature',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u7b7e\u540d'),
        ),
    ]
