# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_auto_20151016_0430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newslikethrough',
            options={'ordering': ('-like_at',)},
        ),
    ]
