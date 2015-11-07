# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(default='1970-01-01 00:00:00', verbose_name='\u53d1\u5e03\u65e5\u671f', auto_now_add=True),
            preserve_default=False,
        ),
    ]
