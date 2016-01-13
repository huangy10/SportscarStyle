# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0009_auto_20151110_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.OneToOneField(related_name='friendship', verbose_name=b'\xe6\x9c\x8b\xe5\x8f\x8b\xe5\x9c\x88\xe5\x88\x9b\xe5\xbb\xba\xe8\x80\x85', to=settings.AUTH_USER_MODEL)),
                ('friend', models.ManyToManyField(related_name='+', verbose_name=b'\xe6\x9c\x8b\xe5\x8f\x8b', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
