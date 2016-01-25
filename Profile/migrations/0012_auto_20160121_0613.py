# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0011_auto_20160121_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='fans',
            field=models.ManyToManyField(related_name='does_not_important_2', verbose_name=b'\xe7\xb2\x89\xe4\xb8\x9d', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='follow',
            field=models.ManyToManyField(related_name='does_not_important_3', verbose_name=b'\xe5\x85\xb3\xe6\xb3\xa8', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='friend',
            field=models.ManyToManyField(related_name='does_not_important_1', verbose_name=b'\xe6\x9c\x8b\xe5\x8f\x8b', to=settings.AUTH_USER_MODEL),
        ),
    ]
