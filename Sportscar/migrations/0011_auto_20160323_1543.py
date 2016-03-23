# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0010_sportscar_remote_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='remote_thumbnail',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u8fdc\u7a0b\u7f29\u7565\u56fe'),
        ),
        migrations.AddField(
            model_name='sportscar',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=Sportscar.models.car_image, verbose_name='\u7f29\u7565\u56fe'),
            preserve_default=False,
        ),
    ]
