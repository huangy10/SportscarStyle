# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='engine',
            field=models.CharField(default='  ', max_length=100, verbose_name='\u53d1\u52a8\u673a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sportscar',
            name='image',
            field=models.ImageField(default='', upload_to=Sportscar.models.car_image, verbose_name='\u8dd1\u8f66\u7167\u7247'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sportscar',
            name='max_speed',
            field=models.CharField(default=100, max_length=20, verbose_name='\u6700\u9ad8\u8f66\u901f'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sportscar',
            name='transmission',
            field=models.CharField(default='a', max_length=100, verbose_name='\u53d8\u901f\u5668'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sportscar',
            name='zeroTo60',
            field=models.CharField(default='3s', max_length=7, verbose_name='\u767e\u516c\u91cc\u52a0\u901f'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='logo',
            field=models.ImageField(upload_to=Sportscar.models.car_logo, verbose_name='\u8f66\u6807'),
        ),
    ]
