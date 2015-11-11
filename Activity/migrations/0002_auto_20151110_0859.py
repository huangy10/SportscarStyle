# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='allowed_club',
            field=models.ForeignKey(verbose_name='\u5141\u8bb8\u52a0\u5165\u7684\u4ff1\u4e50\u90e8', blank=True, to='Club.Club', null=True),
        ),
    ]
