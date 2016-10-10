# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0007_news_is_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='is_video',
            field=custom.fields.BooleanField(default=False, verbose_name='\u5185\u5bb9\u662f\u5426\u662f\u89c6\u9891'),
        ),
    ]
