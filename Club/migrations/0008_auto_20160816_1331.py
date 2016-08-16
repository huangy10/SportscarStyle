# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0007_auto_20160815_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='city',
            field=models.CharField(max_length=30, verbose_name='\u4ff1\u4e50\u90e8\u6240\u5728\u7684\u57ce\u5e02', db_index=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='identified',
            field=models.BooleanField(default=False, db_index=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81'),
        ),
    ]
