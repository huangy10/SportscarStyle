# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0014_userrelationsetting_blacklist_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrelationsetting',
            name='blacklist_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x8b\x89\xe9\xbb\x91\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
