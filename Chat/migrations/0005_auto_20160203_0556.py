# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Club', '0001_initial'),
        ('Chat', '0004_auto_20160131_0604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatrecordbasic',
            name='target_id',
        ),
        migrations.AddField(
            model_name='chatrecordbasic',
            name='target_club',
            field=models.ForeignKey(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\xbe\xa4\xe8\x81\x8a', blank=True, to='Club.Club', null=True),
        ),
        migrations.AddField(
            model_name='chatrecordbasic',
            name='target_user',
            field=models.ForeignKey(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\x94\xa8\xe6\x88\xb7', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='chatrecordbasic',
            name='sender',
            field=models.ForeignKey(related_name='chats', to=settings.AUTH_USER_MODEL),
        ),
    ]
