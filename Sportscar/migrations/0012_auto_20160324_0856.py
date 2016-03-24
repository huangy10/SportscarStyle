# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0011_auto_20160323_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='index',
            field=models.CharField(default='A', max_length=1, verbose_name='\u97f3\u5e8f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='thumbnail',
            field=models.ImageField(upload_to=Sportscar.models.car_thumbnail, verbose_name='\u7f29\u7565\u56fe'),
        ),
    ]
