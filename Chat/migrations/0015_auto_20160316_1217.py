# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0014_auto_20160316_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatrecordbasic',
            name='message_type',
            field=models.CharField(max_length=15, choices=[(b'text', b'text'), (b'image', b'image'), (b'audio', b'audio'), (b'activity', b'activity'), (b'share', b'share'), (b'contact', b'contact'), (b'placeholder', b'placeholder')]),
        ),
    ]
