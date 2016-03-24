# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0012_auto_20160324_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturer',
            name='logo',
            field=models.ImageField(default='', upload_to=Sportscar.models.car_logo, verbose_name='\u5382\u5546logo'),
            preserve_default=False,
        ),
    ]
