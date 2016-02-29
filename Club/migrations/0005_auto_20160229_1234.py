# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0004_clubjoining_chat_sync_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubjoining',
            name='chat_sync_date',
        ),
        migrations.AddField(
            model_name='clubjoining',
            name='unread_chats',
            field=models.IntegerField(default=0, verbose_name='\u672a\u8bfb\u6d88\u606f\u6570\u91cf'),
        ),
    ]
