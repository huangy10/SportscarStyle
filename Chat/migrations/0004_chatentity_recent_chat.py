# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0003_auto_20160503_0457'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatentity',
            name='recent_chat',
            field=models.CharField(default='', max_length=255, verbose_name='\u6700\u8fd1\u4e00\u6761\u804a\u5929\u7684\u5185\u5bb9'),
            preserve_default=False,
        ),
    ]
