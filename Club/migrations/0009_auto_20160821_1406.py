# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0008_auto_20160816_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(related_name='club_joined', verbose_name='\u6210\u5458', through='Club.ClubJoining', to=settings.AUTH_USER_MODEL),
        ),
    ]
