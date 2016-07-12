# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0003_sportscar_price_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportscar',
            name='logo',
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='torque',
            field=models.CharField(default='-', max_length=255, verbose_name='\u626d\u77e9'),
        ),
    ]
