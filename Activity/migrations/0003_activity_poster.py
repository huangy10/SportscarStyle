# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0002_auto_20151110_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='poster',
            field=models.ImageField(default='', upload_to=Activity.models.activity_poster, verbose_name='\u6d3b\u52a8\u6d77\u62a5'),
            preserve_default=False,
        ),
    ]
