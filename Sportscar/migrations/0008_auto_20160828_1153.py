# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0007_auto_20160812_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmediaitem',
            name='link',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u94fe\u63a5'),
        ),
        migrations.AlterField(
            model_name='carmediaitem',
            name='item',
            field=models.FileField(upload_to=Sportscar.models.car_image, null=True, verbose_name='\u5173\u8054\u6587\u4ef6', blank=True),
        ),
    ]
