# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('SettingCenter', '0003_auto_20160918_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingcenter',
            name='notification_accept',
            field=custom.fields.BooleanField(default=True, verbose_name='\u63a5\u53d7\u901a\u77e5'),
        ),
        migrations.AlterField(
            model_name='settingcenter',
            name='notification_shake',
            field=custom.fields.BooleanField(default=True, verbose_name='\u9707\u52a8'),
        ),
        migrations.AlterField(
            model_name='settingcenter',
            name='notification_sound',
            field=custom.fields.BooleanField(default=True, verbose_name='\u58f0\u97f3'),
        ),
        migrations.AlterField(
            model_name='settingcenter',
            name='show_on_map',
            field=custom.fields.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb1\x95\xe7\x8e\xb0\xe5\x9c\xa8\xe5\x9c\xb0\xe5\x9b\xbe\xe4\xb8\x8a'),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='read',
            field=custom.fields.BooleanField(default=False),
        ),
    ]
