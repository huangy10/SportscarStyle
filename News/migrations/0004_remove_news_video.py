# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0003_remove_news_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='video',
        ),
    ]
