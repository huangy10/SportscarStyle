# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='authed_user_only',
            field=models.BooleanField(default=False, verbose_name='\u53ea\u9650\u8ba4\u8bc1\u7528\u6237\u53c2\u52a0'),
        ),
    ]
