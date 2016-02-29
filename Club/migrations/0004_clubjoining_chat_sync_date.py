# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0003_auto_20160228_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubjoining',
            name='chat_sync_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u7fa4\u804a\u76d1\u542c\u65f6\u95f4'),
        ),
    ]
