# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0008_auto_20160226_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatrecordbasic',
            options={'ordering': ('distinct_identifier', '-created_at')},
        ),
    ]
