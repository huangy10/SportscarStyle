# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0004_chatentity_recent_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='audio_length',
            field=models.FloatField(default=0, verbose_name='\u97f3\u9891\u6587\u4ef6\u7684\u957f\u5ea6'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='audio_wave_data',
            field=models.CharField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='chatentity',
            name='club',
            field=models.ForeignKey(related_name='+', verbose_name='\u5173\u8054\u7684\u7fa4\u804a', blank=True, to='Club.Club', null=True),
        ),
    ]
