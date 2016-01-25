# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0002_auto_20160123_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatrecordbasic',
            name='message_type',
            field=models.CharField(max_length=10, choices=[(b'text', b'text'), (b'image', b'image'), (b'voice', b'voice'), (b'activity', b'activity'), (b'share', b'share'), (b'contact', b'contact')]),
        ),
    ]
