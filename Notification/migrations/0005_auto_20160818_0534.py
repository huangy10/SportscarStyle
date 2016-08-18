# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0004_auto_20160512_0401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='message_body',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='message_type',
        ),
        migrations.AddField(
            model_name='notification',
            name='display_mode',
            field=models.CharField(default='minimal', max_length=20, choices=[(b'minimal', b'minimal'), (b'with_cover', b'with_cover'), (b'interact', b'interact')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='extra_info',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='sender_class_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
