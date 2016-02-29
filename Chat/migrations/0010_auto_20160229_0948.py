# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0009_auto_20160226_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='club',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='inform_of',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='user',
        ),
        migrations.AlterField(
            model_name='chatrecordbasic',
            name='target_user',
            field=models.ForeignKey(related_name='chats_to_me', verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\x94\xa8\xe6\x88\xb7', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]
