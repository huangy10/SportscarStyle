# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0013_auto_20160219_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='comment_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activity',
            name='like_num',
            field=models.IntegerField(default=0),
        ),
    ]
