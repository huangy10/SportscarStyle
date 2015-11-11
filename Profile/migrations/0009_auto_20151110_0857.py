# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_auto_20151029_1538'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfollow',
            options={'ordering': ['-created_at'], 'verbose_name': '\u7528\u6237\u5173\u7cfb', 'verbose_name_plural': '\u7528\u6237\u5173\u7cfb'},
        ),
    ]
