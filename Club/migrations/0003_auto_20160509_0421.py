# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='value_average',
        ),
        migrations.RemoveField(
            model_name='club',
            name='value_total',
        ),
    ]
