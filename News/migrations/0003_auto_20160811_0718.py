# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='video',
        ),
        migrations.AddField(
            model_name='news',
            name='is_video',
            field=models.BooleanField(default=False, verbose_name='\u5185\u5bb9\u662f\u5426\u662f\u89c6\u9891'),
        ),
    ]
