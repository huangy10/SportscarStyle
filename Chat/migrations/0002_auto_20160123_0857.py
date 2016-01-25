# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatrecordbasic',
            name='chat_type',
            field=models.CharField(max_length=10, choices=[(b'private', b'private'), (b'group', b'group')]),
        ),
        migrations.AlterField(
            model_name='chatrecordbasic',
            name='message_type',
            field=models.IntegerField(max_length=10, choices=[(b'text', b'text'), (b'image', b'image'), (b'voice', b'voice'), (b'activity', b'activity'), (b'share', b'share'), (b'contact', b'contact')]),
        ),
    ]
