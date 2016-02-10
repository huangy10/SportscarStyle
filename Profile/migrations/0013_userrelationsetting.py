# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0012_auto_20160121_0613'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRelationSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow_see_status', models.BooleanField(default=True, verbose_name=b'\xe5\x85\x81\xe8\xae\xb8\xe6\x9f\xa5\xe7\x9c\x8b\xe6\x88\x91\xe7\x9a\x84\xe5\x8a\xa8\xe6\x80\x81')),
                ('see_his_status', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9f\xa5\xe7\x9c\x8b\xe4\xbb\x96\xe7\x9a\x84\xe5\x8a\xa8\xe6\x80\x81')),
                ('remark_name', models.CharField(max_length=255, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('target', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='relation_settings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
