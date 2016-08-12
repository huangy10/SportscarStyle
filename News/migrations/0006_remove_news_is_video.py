# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0005_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='is_video',
        ),
    ]
