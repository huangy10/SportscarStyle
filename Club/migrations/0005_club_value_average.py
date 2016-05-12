# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0004_club_value_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='value_average',
            field=models.IntegerField(default=0, verbose_name='\u5747\u4ef7'),
        ),
    ]
