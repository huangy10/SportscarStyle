# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0007_chatrecordbasic_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatrecordbasic',
            options={'ordering': ('-created_at',)},
        ),
    ]
