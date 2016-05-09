# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20160503_0453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fans',
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(related_name='fans', through='User.UserRelation', to='User.User'),
        ),
    ]
