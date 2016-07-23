# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0002_auto_20160710_0504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='content',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u6b63\u6587', blank=True),
        ),
    ]
