# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0010_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='fans',
            field=models.ManyToManyField(related_name='+', verbose_name=b'\xe7\xb2\x89\xe4\xb8\x9d', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendship',
            name='follow',
            field=models.ManyToManyField(related_name='+', verbose_name=b'\xe5\x85\xb3\xe6\xb3\xa8', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userfollow',
            unique_together=set([('source_user', 'target_user')]),
        ),
    ]
