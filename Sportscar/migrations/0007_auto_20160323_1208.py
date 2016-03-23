# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0006_auto_20160302_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manufacturer',
            name='name_english',
        ),
        migrations.RemoveField(
            model_name='sportscar',
            name='name_english',
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='detail_url',
            field=models.CharField(default='', max_length=255, verbose_name='\u8be6\u60c5\u94fe\u63a5'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='logo_remote',
            field=models.CharField(default='', max_length=255, verbose_name='\u5382\u5546\u7684logo\u7684url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='remote_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sportscar',
            name='data_fetched',
            field=models.BooleanField(default=False, verbose_name=''),
        ),
        migrations.AddField(
            model_name='sportscar',
            name='torque',
            field=models.CharField(default='-', max_length=255),
        ),
    ]
