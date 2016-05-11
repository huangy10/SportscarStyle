# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='price_number',
            field=models.IntegerField(default=0, verbose_name='\u4ef7\u683c\u6570\u503c'),
        ),
    ]
