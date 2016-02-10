# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0006_auto_20160205_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(default=None, verbose_name='\u6d3b\u52a8\u53d1\u8d77\u8005', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
