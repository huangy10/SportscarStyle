# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0006_chatrecordbasic_distinct_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatrecordbasic',
            name='read',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe8\xaf\xbb'),
        ),
    ]
