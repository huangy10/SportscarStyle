# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0014_auto_20160319_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitylikethrough',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RenameField(
            model_name='activitylikethrough',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
