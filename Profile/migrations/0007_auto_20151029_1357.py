# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0006_auto_20151028_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollow',
            name='source_user',
            field=models.ForeignKey(related_name='+', verbose_name=b'\xe5\x85\xb3\xe6\xb3\xa8\xe8\x80\x85', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userfollow',
            name='target_user',
            field=models.ForeignKey(related_name='+', verbose_name=b'\xe8\xa2\xab\xe5\x85\xb3\xe6\xb3\xa8\xe8\x80\x85', to=settings.AUTH_USER_MODEL),
        ),
    ]
