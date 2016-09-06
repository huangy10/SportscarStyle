# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0008_auto_20160828_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carmediaitem',
            options={'ordering': ('order', 'created_at')},
        ),
        migrations.AddField(
            model_name='carmediaitem',
            name='order',
            field=models.IntegerField(default=0, help_text='\u4ece\u5c0f\u5230\u5927\u6392\u5217', verbose_name='\u6392\u5e8f\u6743\u91cd'),
        ),
        migrations.AlterField(
            model_name='carmediaitem',
            name='link',
            field=models.CharField(default=b'', help_text='\u6b64\u9879\u4e0d\u4e3a\u7a7a\u65f6,\u5c06\u8986\u76d6\u5173\u8054\u6587\u4ef6\u7684\u5185\u5bb9', max_length=255, verbose_name='\u94fe\u63a5', blank=True),
        ),
    ]
