# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0001_initial'),
        ('Profile', '0004_auto_20151003_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_club',
            field=models.ForeignKey(verbose_name='\u8ba4\u8bc1\u4ff1\u4e50\u90e8', blank=True, to='Club.Club', null=True),
        ),
    ]
