# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0005_auto_20160203_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatrecordbasic',
            name='distinct_identifier',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
